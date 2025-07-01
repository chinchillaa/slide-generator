from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add smolagents to path
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "smolagents"))

from app.research_agent import ResearchAgent
from app.slide_generator import SlideGenerator

app = FastAPI(title="Deep Research Slides API")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# グローバル変数
research_agent = None
slide_generator = None
active_connections: List[WebSocket] = []

class ResearchRequest(BaseModel):
    query: str
    model_id: Optional[str] = "gpt-4o"
    max_slides: Optional[int] = 6
    slide_theme: Optional[str] = "default"

class ResearchResponse(BaseModel):
    research_id: str
    status: str
    progress: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    slides_html: Optional[str] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """アプリケーション起動時の初期化"""
    global research_agent, slide_generator
    try:
        research_agent = ResearchAgent()
        slide_generator = SlideGenerator()
        print("✅ Research Agent and Slide Generator initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize: {str(e)}")
        raise

@app.get("/")
async def root():
    return {"message": "Deep Research Slides API", "status": "running"}

@app.post("/research", response_model=ResearchResponse)
async def create_research(request: ResearchRequest):
    """新しい調査リクエストを作成"""
    research_id = f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # バックグラウンドで調査を開始
    asyncio.create_task(
        execute_research(
            research_id=research_id,
            query=request.query,
            model_id=request.model_id,
            max_slides=request.max_slides,
            slide_theme=request.slide_theme
        )
    )
    
    return ResearchResponse(
        research_id=research_id,
        status="started",
        progress=0
    )

async def execute_research(
    research_id: str, 
    query: str, 
    model_id: str,
    max_slides: int,
    slide_theme: str
):
    """調査を実行し、結果をスライド化"""
    try:
        print(f"Starting research for {research_id}")
        print(f"Active connections: {len(active_connections)}")
        
        # WebSocket経由で進捗を送信
        await broadcast_progress(
            research_id=research_id,
            status="researching",
            progress=10,
            message="調査を開始しています..."
        )
        print("Initial progress sent")
        
        # ツール実行時のコールバック関数
        async def tool_callback(tool_info):
            """ツールの実行状況をWebSocketで送信"""
            status_message = ""
            details = {}
            
            # LLMの思考過程の場合
            if tool_info.get("tool_name") == "agent_thinking":
                status_message = "🤔 思考中..."
                details["agent_thinking"] = tool_info.get('agent_thinking', '')
                details["thinking_timestamp"] = tool_info.get('thinking_timestamp', 0)
            # ツール実行の場合
            elif tool_info.get("tool_name") == "web_search":
                if tool_info["status"] == "started":
                    status_message = f"🔍 検索中: {tool_info.get('query', '')}"
                    details["action"] = "searching"
                    details["query"] = tool_info.get('query', '')
                elif tool_info["status"] == "completed":
                    status_message = f"✅ 検索完了"
                    if "found_urls" in tool_info:
                        details["found_urls"] = tool_info["found_urls"]
                        
            elif tool_info.get("tool_name") == "visit_page":
                if tool_info["status"] == "started":
                    url = tool_info.get('url', '')
                    status_message = f"🌐 アクセス中: {url}"
                    details["action"] = "visiting"
                    details["url"] = url
                elif tool_info["status"] == "completed":
                    status_message = f"✅ ページ取得完了"
                    
            elif tool_info.get("status") == "error":
                status_message = f"❌ エラー: {tool_info.get('error', '')}"
                details["error"] = tool_info.get('error', '')
            
            # ツールの実行状況を送信
            if status_message:
                await broadcast_progress(
                    research_id=research_id,
                    status="researching",
                    progress=15,
                    message=status_message,
                    tool_activity=details
                )
        
        # コールバック付きでResearchAgentを作成
        research_agent_with_callback = ResearchAgent(
            progress_callback=lambda info: asyncio.create_task(tool_callback(info))
        )
        
        # Deep Researchで調査実行（別タスクで実行）
        research_task = asyncio.create_task(
            research_agent_with_callback.run_research(query, model_id)
        )
        
        # 進捗を定期的に更新
        progress = 10
        while not research_task.done():
            await asyncio.sleep(2)  # 2秒ごとに更新
            progress = min(progress + 5, 45)  # 最大45%まで
            await broadcast_progress(
                research_id=research_id,
                status="researching",
                progress=progress,
                message="調査を実行中です..."
            )
        
        # 結果を取得
        research_result = await research_task
        
        await broadcast_progress(
            research_id=research_id,
            status="researching",
            progress=50,
            message="調査が完了しました"
        )
        
        # 調査結果をスライド化
        await broadcast_progress(
            research_id=research_id,
            status="generating_slides",
            progress=60,
            message="スライドを生成しています..."
        )
        
        slides_html = await slide_generator.generate_slides(
            research_result=research_result,
            query=query,
            max_slides=max_slides,
            theme=slide_theme
        )
        
        await broadcast_progress(
            research_id=research_id,
            status="completed",
            progress=100,
            message="完了しました",
            result=research_result,
            slides_html=slides_html
        )
        
    except Exception as e:
        await broadcast_progress(
            research_id=research_id,
            status="error",
            progress=0,
            message=f"エラーが発生しました: {str(e)}",
            error=str(e)
        )

async def broadcast_progress(
    research_id: str,
    status: str,
    progress: int,
    message: str,
    result: Optional[Dict] = None,
    slides_html: Optional[str] = None,
    error: Optional[str] = None,
    tool_activity: Optional[Dict] = None
):
    """WebSocket経由で進捗を配信"""
    data = {
        "research_id": research_id,
        "status": status,
        "progress": progress,
        "message": message,
        "result": result,
        "slides_html": slides_html,
        "error": error,
        "tool_activity": tool_activity
    }
    
    print(f"Broadcasting: {status} - {progress}% - {message}")
    print(f"To {len(active_connections)} connections")
    
    for connection in active_connections:
        try:
            await connection.send_json(data)
            print("Message sent successfully")
        except Exception as e:
            print(f"Failed to send: {e}")
            # 接続が切れている場合は削除
            active_connections.remove(connection)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocketエンドポイント"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # クライアントからのメッセージを待機
            data = await websocket.receive_text()
            # 必要に応じて処理
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "research_agent": research_agent is not None,
        "slide_generator": slide_generator is not None,
        "active_connections": len(active_connections)
    }