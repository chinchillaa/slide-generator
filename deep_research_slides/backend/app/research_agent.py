import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import asyncio
from dotenv import load_dotenv
import io
import contextlib
import threading
import queue
import time

# smolagentsのパスを追加
smolagents_path = Path(__file__).parent.parent.parent.parent / "smolagents"
sys.path.insert(0, str(smolagents_path))

from smolagents import (
    CodeAgent,
    LiteLLMModel,
    ToolCallingAgent,
    Tool,
)
from smolagents.default_tools import DuckDuckGoSearchTool, GoogleSearchTool

# Deep Research用のツールをインポート
sys.path.insert(0, str(smolagents_path / "examples" / "open_deep_research"))
from scripts.text_inspector_tool import TextInspectorTool
from scripts.text_web_browser import (
    ArchiveSearchTool,
    FinderTool,
    FindNextTool,
    PageDownTool,
    PageUpTool,
    SimpleTextBrowser,
    VisitTool,
)

load_dotenv()

class MonitoredToolWrapper:
    """ツールの実行をモニタリングするラッパークラス"""
    def __init__(self, tool, callback=None):
        self.wrapped_tool = tool
        self.callback = callback
        
        # 元のツールのすべての属性をコピー
        for attr_name in dir(tool):
            if not attr_name.startswith('_'):
                attr_value = getattr(tool, attr_name)
                if not callable(attr_value) or attr_name == 'forward':
                    setattr(self, attr_name, attr_value)
        
        # forwardメソッドを特別に処理
        self._setup_monitored_forward()
    
    def _setup_monitored_forward(self):
        """forwardメソッドをモニタリング機能付きでラップ"""
        import inspect
        from functools import wraps
        
        original_forward = self.wrapped_tool.forward
        original_sig = inspect.signature(original_forward)
        
        @wraps(original_forward)
        def monitored_forward(*args, **kwargs):
            # バインドされた引数を取得
            try:
                bound_args = original_sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
            except:
                # バインドエラーの場合はそのまま実行
                return original_forward(*args, **kwargs)
            
            # 実行前にコールバック
            if self.callback:
                tool_info = {
                    "tool_name": self.name,
                    "status": "started",
                    "args": bound_args.args,
                    "kwargs": bound_args.kwargs
                }
                
                # 特定のツールの引数を抽出
                if self.name == "visit_page" and "url" in bound_args.arguments:
                    tool_info["url"] = bound_args.arguments["url"]
                elif self.name == "web_search" and "query" in bound_args.arguments:
                    tool_info["query"] = bound_args.arguments["query"]
                    
                self.callback(tool_info)
            
            # ツールを実行
            try:
                result = original_forward(*args, **kwargs)
                
                # 実行後にコールバック
                if self.callback:
                    tool_info = {
                        "tool_name": self.name,
                        "status": "completed",
                        "result_preview": str(result)[:200] if result else None
                    }
                    
                    # GoogleSearchToolの結果からURLを抽出
                    if self.name == "web_search" and result:
                        try:
                            # 結果からURLを抽出（実装はツールの出力形式に依存）
                            if isinstance(result, list):
                                tool_info["found_urls"] = [item.get("link", "") for item in result if "link" in item]
                        except:
                            pass
                            
                    self.callback(tool_info)
                    
                return result
                
            except Exception as e:
                # エラー時にもコールバック
                if self.callback:
                    self.callback({
                        "tool_name": self.name,
                        "status": "error",
                        "error": str(e)
                    })
                raise
        
        # 元のシグネチャを保持した新しいforwardメソッドを設定
        monitored_forward.__signature__ = original_sig
        self.forward = monitored_forward
    
    def __getattr__(self, name):
        """定義されていない属性は元のツールから取得"""
        return getattr(self.wrapped_tool, name)

class ThinkingCapture:
    """エージェントの思考過程をキャプチャするクラス"""
    def __init__(self, callback=None):
        self.callback = callback
        self.buffer = io.StringIO()
        self.captured_lines = []
        
    def write(self, text):
        """標準出力のwrite()をオーバーライド"""
        # 元の標準出力にも書き込み
        sys.__stdout__.write(text)
        
        # バッファに書き込み
        self.buffer.write(text)
        
        # 改行で区切って保存
        if '\n' in text:
            content = self.buffer.getvalue()
            if content.strip():
                # 内容を保存
                self.captured_lines.append(content)
                # コールバックを直接呼び出す（asyncio.create_taskは呼び出し側で処理）
                if self.callback:
                    self.callback({
                        "tool_name": "agent_thinking",
                        "status": "thinking",
                        "agent_thinking": content,
                        "thinking_timestamp": time.time()
                    })
            self.buffer = io.StringIO()
    
    def flush(self):
        """標準出力のflush()をオーバーライド"""
        sys.__stdout__.flush()
    
    def get_all_output(self):
        """キャプチャしたすべての出力を取得"""
        return self.captured_lines

class ResearchAgent:
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.browser_config = {
            "viewport_size": 1024 * 5,
            "downloads_folder": "downloads_folder",
            "request_kwargs": {
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                "timeout": 300,
            },
        }
        
        # ダウンロードフォルダの作成
        os.makedirs(self.browser_config['downloads_folder'], exist_ok=True)
        
    def create_agent(self, model_id: str = "gpt-4o") -> CodeAgent:
        """Deep Researchエージェントを作成"""
        # カスタムロール変換
        custom_role_conversions = {"tool-call": "assistant", "tool-response": "user"}
        
        # モデルの設定
        model_params = {
            "model_id": model_id,
            "custom_role_conversions": custom_role_conversions,
            "max_completion_tokens": 4096,
        }
        
        model = LiteLLMModel(**model_params)
        
        # ブラウザとツールの設定
        text_limit = 100000
        browser = SimpleTextBrowser(**self.browser_config)
        
        # ツールを作成してモニタリングラッパーでラップ
        raw_tools = [
            DuckDuckGoSearchTool(),  # DuckDuckGoを使用（APIキー不要）
            VisitTool(browser),
            PageUpTool(browser),
            PageDownTool(browser),
            FinderTool(browser),
            FindNextTool(browser),
            ArchiveSearchTool(browser),
            TextInspectorTool(model, text_limit),
        ]
        
        # 一時的にモニタリング機能を無効化
        web_tools = raw_tools
        
        # # コールバックがある場合はツールをラップ
        # if self.progress_callback:
        #     web_tools = [MonitoredToolWrapper(tool, self.progress_callback) for tool in raw_tools]
        # else:
        #     web_tools = raw_tools
        
        # Web検索エージェント
        text_webbrowser_agent = ToolCallingAgent(
            model=model,
            tools=web_tools,
            max_steps=15,
            verbosity_level=2,  # 詳細なログを出力
            planning_interval=3,
            name="search_agent",
            description="""インターネットを検索して質問に答えるチームメンバー。
            Web検索が必要な質問はすべて彼に聞いてください。
            できるだけ多くのコンテキストを提供してください。特に特定の期間で検索する必要がある場合は重要です。
            複雑な検索タスクも遠慮なく依頼してください。""",
            provide_run_summary=True,
        )
        
        # マネージャーエージェント
        manager_agent = CodeAgent(
            model=model,
            tools=[TextInspectorTool(model, text_limit)],
            max_steps=10,
            verbosity_level=1,
            additional_authorized_imports=["*"],
            planning_interval=3,
            managed_agents=[text_webbrowser_agent],
        )
        
        return manager_agent
    
    async def run_research(self, query: str, model_id: str = "gpt-4o") -> Dict[str, Any]:
        """調査を実行"""
        thinking_capture = None
        try:
            # エージェントを作成
            agent = self.create_agent(model_id)
            
            # 調査用のプロンプトを構築
            research_prompt = f"""
            以下のトピックについて詳細な調査を行ってください：
            
            {query}
            
            調査では以下の点を含めてください：
            1. 背景と概要
            2. 主要な事実とデータ
            3. 重要なポイントと洞察
            4. 関連する統計やトレンド
            5. 信頼できる情報源
            
            できるだけ具体的で、データに基づいた情報を収集してください。
            """
            
            # 思考過程をキャプチャする設定
            if self.progress_callback:
                thinking_capture = ThinkingCapture(self.progress_callback)
                # 標準出力をリダイレクト
                old_stdout = sys.stdout
                sys.stdout = thinking_capture
            
            try:
                # エージェントの実行
                result = agent.run(research_prompt)
            finally:
                # 標準出力を元に戻す
                if thinking_capture:
                    sys.stdout = old_stdout
            
            # 結果を構造化
            research_result = {
                "query": query,
                "raw_result": result,
                "sections": self._parse_research_result(result),
                "sources": self._extract_sources(result),
            }
            
            return research_result
            
        except Exception as e:
            # エラー時も標準出力を元に戻す
            if thinking_capture and 'old_stdout' in locals():
                sys.stdout = old_stdout
            raise Exception(f"Research failed: {str(e)}")
    
    def _parse_research_result(self, result: str) -> Dict[str, Any]:
        """調査結果を構造化されたセクションに分割"""
        sections = {
            "overview": "",
            "key_facts": [],
            "insights": [],
            "statistics": [],
            "trends": [],
        }
        
        # シンプルなパーシング（実際の実装では、より高度な処理が必要）
        lines = result.strip().split('\n')
        current_section = "overview"
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # セクションの検出
            if "背景" in line or "概要" in line:
                current_section = "overview"
            elif "事実" in line or "データ" in line:
                current_section = "key_facts"
            elif "ポイント" in line or "洞察" in line:
                current_section = "insights"
            elif "統計" in line:
                current_section = "statistics"
            elif "トレンド" in line:
                current_section = "trends"
            else:
                # コンテンツの追加
                if current_section == "overview":
                    sections["overview"] += line + "\n"
                elif current_section in ["key_facts", "insights", "statistics", "trends"]:
                    if line.startswith("・") or line.startswith("-") or line.startswith("•"):
                        sections[current_section].append(line[1:].strip())
        
        return sections
    
    def _extract_sources(self, result: str) -> List[str]:
        """結果から情報源を抽出"""
        sources = []
        
        # URLパターンの検出（シンプルな実装）
        import re
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, result)
        
        for url in urls:
            if url not in sources:
                sources.append(url)
        
        return sources[:10]  # 最大10個まで