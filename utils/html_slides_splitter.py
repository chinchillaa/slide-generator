#!/usr/bin/env python3
"""
HTMLスライドを個別ファイルに分割するツール
各スライドを印刷可能な個別HTMLファイルとして出力
"""

import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import shutil
from datetime import datetime


def extract_and_save_slides(html_file_path, output_dir):
    """
    HTMLファイルから各スライドを抽出して個別ファイルとして保存
    
    Args:
        html_file_path: 入力HTMLファイルのパス
        output_dir: 出力ディレクトリのパス
        
    Returns:
        生成されたHTMLファイルの情報リスト
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # スタイルとリンクを保持
    styles = []
    for style in soup.find_all('style'):
        styles.append(str(style))
    
    css_links = []
    for link in soup.find_all('link', rel='stylesheet'):
        css_links.append(str(link))
    
    # Font Awesomeが含まれていることを確認
    if not any('fontawesome' in str(link) for link in css_links):
        css_links.append('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">')
    
    # Tailwindが含まれていることを確認
    if not any('tailwind' in str(link) for link in css_links):
        css_links.append('<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">')
    
    # スライドコンテナを取得
    slides = soup.find_all('div', class_='slide-container')
    
    if not slides:
        print("エラー: スライドが見つかりません")
        return []
    
    slide_info = []
    
    for i, slide in enumerate(slides, 1):
        # スライドのタイトルを抽出（最初のh1またはh2）
        title_elem = slide.find(['h1', 'h2'])
        title = title_elem.get_text(strip=True) if title_elem else f"スライド {i}"
        
        # 各スライド用のHTMLを作成
        slide_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - スライド {i}</title>
    {''.join(css_links)}
    <style>
        /* 基本スタイル */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Hiragino Sans', 'Meiryo', 'Arial', sans-serif;
            background-color: #f3f4f6;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        
        /* スライドコンテナ */
        .slide-container {{
            width: 1280px !important;
            height: 720px !important;
            background-color: white !important;
            position: relative !important;
            overflow: hidden !important;
            display: block !important;
            margin: 20px auto !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }}
        
        /* ナビゲーションを非表示 */
        .navigation {{
            display: none !important;
        }}
        
        /* 印刷用スタイル */
        @media print {{
            body {{
                margin: 0;
                padding: 0;
                background-color: white;
            }}
            
            .slide-container {{
                width: 100vw !important;
                height: 100vh !important;
                margin: 0 !important;
                box-shadow: none !important;
                page-break-after: avoid;
                page-break-inside: avoid;
            }}
            
            .print-info {{
                display: none !important;
            }}
        }}
        
        /* 印刷情報 */
        .print-info {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #22c55e;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        @page {{
            size: A4 landscape;
            margin: 0;
        }}
    </style>
    {''.join(styles)}
</head>
<body>
    {str(slide)}
    <div class="print-info">
        印刷するには Ctrl+P (Windows) または Cmd+P (Mac) を押してください
    </div>
</body>
</html>"""
        
        # ファイル名を作成
        filename = f"slide_{i:02d}_{title[:30].replace(' ', '_').replace('/', '_')}.html"
        file_path = os.path.join(output_dir, filename)
        
        # HTMLファイルを保存
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(slide_html)
        
        slide_info.append({
            'index': i,
            'title': title,
            'filename': filename,
            'path': file_path
        })
        
        print(f"✓ スライド {i} を保存: {filename}")
    
    return slide_info


def create_index_page(slide_info, output_dir, original_file):
    """
    スライド一覧のインデックスページを作成
    
    Args:
        slide_info: スライド情報のリスト
        output_dir: 出力ディレクトリのパス
        original_file: 元のHTMLファイル名
    """
    index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>スライド一覧 - {Path(original_file).stem}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <style>
        body {{
            font-family: 'Hiragino Sans', 'Meiryo', 'Arial', sans-serif;
        }}
        .slide-link {{
            transition: all 0.3s ease;
        }}
        .slide-link:hover {{
            background-color: #f0fdf4;
            border-color: #22c55e;
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(34, 197, 94, 0.1);
        }}
    </style>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <div class="bg-white rounded-lg shadow-lg p-8">
            <div class="border-l-4 border-green-500 pl-4 mb-8">
                <h1 class="text-3xl font-bold text-gray-800 mb-2">スライド一覧</h1>
                <p class="text-gray-600">元ファイル: {Path(original_file).name}</p>
                <p class="text-sm text-gray-500">生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}</p>
            </div>
            
            <div class="bg-green-50 border border-green-200 rounded-lg p-6 mb-8">
                <h2 class="text-xl font-bold text-green-800 mb-3">
                    <i class="fas fa-print mr-2"></i>PDFとして印刷する方法
                </h2>
                <ol class="list-decimal list-inside space-y-2 text-gray-700">
                    <li>下記のスライドリンクをクリックして開く</li>
                    <li><kbd class="px-2 py-1 bg-gray-200 rounded">Ctrl+P</kbd> (Windows) または <kbd class="px-2 py-1 bg-gray-200 rounded">Cmd+P</kbd> (Mac) を押す</li>
                    <li>「送信先」で「PDFとして保存」を選択</li>
                    <li>「レイアウト」を「横向き」に設定</li>
                    <li>「余白」を「なし」に設定</li>
                    <li>「保存」をクリック</li>
                </ol>
            </div>
            
            <div class="space-y-4">
                <h2 class="text-2xl font-bold text-gray-800 mb-4">
                    <i class="fas fa-list mr-2 text-green-600"></i>スライド一覧
                </h2>
"""
    
    for info in slide_info:
        index_html += f"""
                <a href="{info['filename']}" target="_blank" 
                   class="block slide-link border border-gray-200 rounded-lg p-4 hover:no-underline">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <div class="bg-green-100 text-green-800 rounded-full w-10 h-10 flex items-center justify-center font-bold mr-4">
                                {info['index']}
                            </div>
                            <div>
                                <h3 class="text-lg font-semibold text-gray-800">{info['title']}</h3>
                                <p class="text-sm text-gray-500">{info['filename']}</p>
                            </div>
                        </div>
                        <i class="fas fa-external-link-alt text-gray-400"></i>
                    </div>
                </a>
"""
    
    index_html += """
            </div>
            
            <div class="mt-8 pt-8 border-t border-gray-200">
                <p class="text-center text-gray-500 text-sm">
                    <i class="fas fa-info-circle mr-1"></i>
                    各スライドは個別のHTMLファイルとして保存されています。
                    印刷時は横向き・余白なしの設定を推奨します。
                </p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"\n✓ インデックスページを作成: {index_path}")


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_splitter.py <HTMLファイル>")
        sys.exit(1)
    
    html_file = Path(sys.argv[1]).absolute()
    
    if not html_file.exists():
        print(f"エラー: HTMLファイルが見つかりません: {html_file}")
        sys.exit(1)
    
    # 出力ディレクトリを.claude/tempに作成
    output_dir = Path("/home/chinchilla/work/slide_generator/.claude/temp") / f"slides_{html_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"出力ディレクトリ: {output_dir}")
    print(f"HTMLファイルを分割中: {html_file}")
    print("-" * 50)
    
    # スライドを分割して保存
    slide_info = extract_and_save_slides(html_file, output_dir)
    
    if not slide_info:
        print("エラー: スライドの分割に失敗しました")
        sys.exit(1)
    
    # インデックスページを作成
    create_index_page(slide_info, output_dir, html_file)
    
    print("\n" + "=" * 50)
    print(f"✅ 完了！{len(slide_info)} 個のスライドを分割しました")
    print(f"📁 出力先: {output_dir}")
    print(f"🌐 インデックスページ: {output_dir}/index.html")
    print("\nブラウザでindex.htmlを開いて、各スライドを印刷してください。")


if __name__ == "__main__":
    main()