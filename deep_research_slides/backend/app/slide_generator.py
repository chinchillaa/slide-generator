from typing import Dict, Any, List, Optional
from pathlib import Path
import json
from datetime import datetime
from jinja2 import Template

class SlideGenerator:
    def __init__(self):
        self.template_path = Path(__file__).parent / "templates"
        self.template_path.mkdir(exist_ok=True)
        
    async def generate_slides(
        self,
        research_result: Dict[str, Any],
        query: str,
        max_slides: int = 6,
        theme: str = "default"
    ) -> str:
        """調査結果からスライドを生成"""
        
        # スライドデータを構造化
        slides_data = self._structure_slides_data(research_result, query, max_slides)
        
        # HTMLテンプレートを使用してスライドを生成
        html_content = self._render_slides_html(slides_data, theme)
        
        return html_content
    
    def _structure_slides_data(
        self,
        research_result: Dict[str, Any],
        query: str,
        max_slides: int
    ) -> List[Dict[str, Any]]:
        """調査結果をスライド形式に構造化"""
        slides = []
        sections = research_result.get("sections", {})
        
        # スライド1: タイトルページ
        slides.append({
            "type": "title",
            "title": query,
            "subtitle": "Deep Research 調査結果",
            "date": datetime.now().strftime("%Y年%m月%d日"),
        })
        
        # スライド2: 概要
        if sections.get("overview"):
            slides.append({
                "type": "overview",
                "title": "概要",
                "content": sections["overview"],
                "icon": "fa-info-circle"
            })
        
        # スライド3: 主要な事実
        if sections.get("key_facts") and len(sections["key_facts"]) > 0:
            slides.append({
                "type": "key_facts",
                "title": "主要な事実",
                "facts": sections["key_facts"][:6],  # 最大6項目
                "icon": "fa-list-check"
            })
        
        # スライド4: 洞察・インサイト
        if sections.get("insights") and len(sections["insights"]) > 0:
            slides.append({
                "type": "insights",
                "title": "重要な洞察",
                "insights": sections["insights"][:4],  # 最大4項目
                "icon": "fa-lightbulb"
            })
        
        # スライド5: 統計データ
        if sections.get("statistics") and len(sections["statistics"]) > 0:
            slides.append({
                "type": "statistics",
                "title": "統計データ",
                "stats": self._format_statistics(sections["statistics"]),
                "icon": "fa-chart-bar"
            })
        
        # スライド6: まとめと情報源
        slides.append({
            "type": "summary",
            "title": "まとめ",
            "summary": self._generate_summary(research_result),
            "sources": research_result.get("sources", [])[:5],  # 最大5つの情報源
        })
        
        # 最大スライド数に調整
        return slides[:max_slides]
    
    def _format_statistics(self, statistics: List[str]) -> List[Dict[str, Any]]:
        """統計データをフォーマット"""
        formatted_stats = []
        
        for stat in statistics[:4]:  # 最大4つ
            # 数値と説明を分離する簡単な処理
            if ":" in stat:
                label, value = stat.split(":", 1)
                formatted_stats.append({
                    "label": label.strip(),
                    "value": value.strip(),
                    "trend": "up" if any(word in stat.lower() for word in ["増加", "上昇", "成長"]) else "neutral"
                })
            else:
                formatted_stats.append({
                    "label": stat,
                    "value": "",
                    "trend": "neutral"
                })
        
        return formatted_stats
    
    def _generate_summary(self, research_result: Dict[str, Any]) -> str:
        """調査結果のサマリーを生成"""
        sections = research_result.get("sections", {})
        
        summary_parts = []
        
        if sections.get("overview"):
            summary_parts.append(sections["overview"][:200] + "...")
        
        if sections.get("key_facts"):
            summary_parts.append(f"主要な事実: {len(sections['key_facts'])}項目を特定")
        
        if sections.get("insights"):
            summary_parts.append(f"重要な洞察: {len(sections['insights'])}点を発見")
        
        return " ".join(summary_parts) if summary_parts else "調査が完了しました。"
    
    def _render_slides_html(self, slides_data: List[Dict[str, Any]], theme: str) -> str:
        """スライドデータをHTMLに変換"""
        html_template = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deep Research Results</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        body {
            font-family: 'Hiragino Sans', 'Meiryo', sans-serif;
            background-color: #f3f4f6;
        }
        .slide {
            width: 1280px;
            height: 720px;
            background: white;
            position: relative;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            display: none;
        }
        .slide.active {
            display: block;
        }
        .logo {
            position: absolute;
            top: 20px;
            right: 20px;
            font-weight: bold;
            color: #888;
            font-size: 24px;
        }
        .title-box {
            border-left: 8px solid #8a2be2;
            padding-left: 20px;
            margin-bottom: 30px;
        }
        .icon-circle {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: rgba(138, 43, 226, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #8a2be2;
        }
        .stat-value {
            color: #8a2be2;
            font-size: 2rem;
            font-weight: bold;
        }
        .navigation {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 20px;
            z-index: 100;
        }
        .nav-btn {
            padding: 10px 20px;
            background: #8a2be2;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .nav-btn:hover {
            background: #7a1ed2;
        }
        .nav-btn:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
    </style>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto py-8">
        <div id="slides-container" class="relative mx-auto">
            {% for slide in slides %}
            <div class="slide {% if loop.first %}active{% endif %}" data-slide="{{ loop.index }}">
                <div class="logo flex items-center">
                    <span class="text-gray-400 mr-2">=</span>SB C&S
                </div>
                
                {% if slide.type == "title" %}
                <!-- タイトルスライド -->
                <div class="h-full flex flex-col justify-center items-center">
                    <div class="text-center">
                        <div class="title-box mb-8">
                            <h1 class="text-5xl font-bold text-gray-800 mb-4">{{ slide.title }}</h1>
                            <p class="text-3xl text-purple-800">{{ slide.subtitle }}</p>
                        </div>
                        <p class="text-xl text-gray-600 mt-8">{{ slide.date }}</p>
                    </div>
                </div>
                
                {% elif slide.type == "overview" %}
                <!-- 概要スライド -->
                <div class="title-box mb-8">
                    <h2 class="text-3xl font-bold text-gray-800 flex items-center">
                        <div class="icon-circle mr-4">
                            <i class="fas {{ slide.icon }}"></i>
                        </div>
                        {{ slide.title }}
                    </h2>
                </div>
                <div class="text-lg leading-relaxed text-gray-700">
                    {{ slide.content }}
                </div>
                
                {% elif slide.type == "key_facts" %}
                <!-- 主要事実スライド -->
                <div class="title-box mb-8">
                    <h2 class="text-3xl font-bold text-gray-800 flex items-center">
                        <div class="icon-circle mr-4">
                            <i class="fas {{ slide.icon }}"></i>
                        </div>
                        {{ slide.title }}
                    </h2>
                </div>
                <div class="grid grid-cols-2 gap-6">
                    {% for fact in slide.facts %}
                    <div class="flex items-start space-x-3">
                        <i class="fas fa-check-circle text-purple-600 mt-1"></i>
                        <p class="text-gray-700">{{ fact }}</p>
                    </div>
                    {% endfor %}
                </div>
                
                {% elif slide.type == "insights" %}
                <!-- 洞察スライド -->
                <div class="title-box mb-8">
                    <h2 class="text-3xl font-bold text-gray-800 flex items-center">
                        <div class="icon-circle mr-4">
                            <i class="fas {{ slide.icon }}"></i>
                        </div>
                        {{ slide.title }}
                    </h2>
                </div>
                <div class="grid grid-cols-2 gap-8">
                    {% for insight in slide.insights %}
                    <div class="bg-purple-50 p-6 rounded-lg border border-purple-200">
                        <div class="flex items-start">
                            <div class="icon-circle mr-4 flex-shrink-0">
                                <i class="fas fa-lightbulb"></i>
                            </div>
                            <p class="text-gray-700">{{ insight }}</p>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                
                {% elif slide.type == "statistics" %}
                <!-- 統計スライド -->
                <div class="title-box mb-8">
                    <h2 class="text-3xl font-bold text-gray-800 flex items-center">
                        <div class="icon-circle mr-4">
                            <i class="fas {{ slide.icon }}"></i>
                        </div>
                        {{ slide.title }}
                    </h2>
                </div>
                <div class="grid grid-cols-2 gap-8">
                    {% for stat in slide.stats %}
                    <div class="bg-gray-50 p-6 rounded-lg border border-gray-200">
                        <p class="text-gray-600 mb-2">{{ stat.label }}</p>
                        <p class="stat-value">{{ stat.value }}</p>
                        {% if stat.trend == "up" %}
                        <i class="fas fa-arrow-up text-green-500"></i>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
                
                {% elif slide.type == "summary" %}
                <!-- まとめスライド -->
                <div class="title-box mb-8">
                    <h2 class="text-3xl font-bold text-gray-800">{{ slide.title }}</h2>
                </div>
                <div class="mb-8">
                    <p class="text-lg text-gray-700 leading-relaxed">{{ slide.summary }}</p>
                </div>
                {% if slide.sources %}
                <div class="mt-8 pt-8 border-t border-gray-200">
                    <h3 class="text-xl font-bold text-gray-700 mb-4">情報源</h3>
                    <ul class="space-y-2">
                        {% for source in slide.sources %}
                        <li class="text-sm text-gray-600">
                            <i class="fas fa-link mr-2"></i>
                            <a href="{{ source }}" class="text-purple-600 hover:underline" target="_blank">
                                {{ source[:60] }}{% if source|length > 60 %}...{% endif %}
                            </a>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
                {% endif %}
                
                {% endif %}
            </div>
            {% endfor %}
        </div>
        
        <!-- ナビゲーション -->
        <div class="navigation">
            <button class="nav-btn" onclick="previousSlide()">
                <i class="fas fa-chevron-left mr-2"></i>前へ
            </button>
            <span class="text-gray-700 flex items-center">
                <span id="current-slide">1</span> / <span id="total-slides">{{ slides|length }}</span>
            </span>
            <button class="nav-btn" onclick="nextSlide()">
                次へ<i class="fas fa-chevron-right ml-2"></i>
            </button>
        </div>
    </div>
    
    <script>
        let currentSlide = 1;
        const totalSlides = {{ slides|length }};
        
        function showSlide(n) {
            const slides = document.querySelectorAll('.slide');
            if (n > totalSlides) currentSlide = totalSlides;
            if (n < 1) currentSlide = 1;
            
            slides.forEach(slide => slide.classList.remove('active'));
            slides[currentSlide - 1].classList.add('active');
            
            document.getElementById('current-slide').textContent = currentSlide;
            
            // ボタンの有効/無効を更新
            document.querySelector('button[onclick="previousSlide()"]').disabled = currentSlide === 1;
            document.querySelector('button[onclick="nextSlide()"]').disabled = currentSlide === totalSlides;
        }
        
        function nextSlide() {
            showSlide(currentSlide += 1);
        }
        
        function previousSlide() {
            showSlide(currentSlide -= 1);
        }
        
        // キーボードナビゲーション
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') previousSlide();
        });
        
        // 初期表示
        showSlide(1);
    </script>
</body>
</html>
        """
        
        template = Template(html_template)
        return template.render(slides=slides_data)