#!/usr/bin/env python3
"""
HTMLスライドをPDFに変換するツール（改良版）
WeasyPrintを使用してHTMLファイルをPDFに変換します
"""

import os
import sys
from pathlib import Path
from weasyprint import HTML, CSS
import re


def create_combined_html(html_content):
    """
    すべてのスライドを含む単一のHTMLを作成
    """
    # 基本的なHTML構造を抽出
    head_match = re.search(r'<head>(.*?)</head>', html_content, re.DOTALL)
    head_content = head_match.group(1) if head_match else ''
    
    # スタイルタグを抽出
    style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    style_content = style_match.group(1) if style_match else ''
    
    # bodyの内容を抽出（ナビゲーションを除く）
    body_match = re.search(r'<body>(.*?)<!-- ナビゲーション', html_content, re.DOTALL)
    if not body_match:
        body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    body_content = body_match.group(1) if body_match else ''
    
    # 各スライドコンテナを表示状態に変更
    body_content = re.sub(r'class="slide-container"', 'class="slide-container active"', body_content)
    body_content = re.sub(r'class="slide-container active"', 'class="slide-container active"', body_content)
    
    # 結合されたHTMLを作成
    combined_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
{head_content}
<style>
{style_content}
/* PDF用の追加スタイル */
@page {{
    size: A4 landscape;
    margin: 0;
}}
body {{
    margin: 0;
    padding: 0;
}}
.slide-container {{
    display: block !important;
    page-break-after: always;
    page-break-inside: avoid;
    width: 297mm;
    height: 210mm;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    overflow: hidden;
    position: relative;
}}
.navigation {{
    display: none !important;
}}
/* 最後のスライドには改ページを追加しない */
.slide-container:last-of-type {{
    page-break-after: auto;
}}
</style>
</head>
<body>
{body_content}
</body>
</html>
"""
    
    return combined_html


def html_to_pdf(html_path, pdf_path):
    """
    HTMLファイルをPDFに変換
    
    Args:
        html_path: 入力HTMLファイルのパス
        pdf_path: 出力PDFファイルのパス
    """
    print(f"HTMLファイルを読み込み中: {html_path}")
    
    # HTMLファイルを読み込む
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # すべてのスライドを含む単一のHTMLを作成
    combined_html = create_combined_html(html_content)
    
    # スライド数をカウント
    slide_count = len(re.findall(r'class="slide-container', combined_html))
    print(f"見つかったスライド数: {slide_count}")
    
    if slide_count == 0:
        print("エラー: スライドが見つかりませんでした")
        return
    
    print("PDFを生成中...")
    
    try:
        # WeasyPrintでPDFを生成
        HTML(string=combined_html, base_url=os.path.dirname(os.path.abspath(html_path))).write_pdf(
            pdf_path
        )
        
        print(f"PDFを保存しました: {pdf_path}")
        
    except Exception as e:
        print(f"PDF生成中にエラーが発生しました: {e}")


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_to_pdf_v2.py <HTMLファイルパス> [PDFファイルパス]")
        sys.exit(1)
    
    html_path = sys.argv[1]
    
    # PDFパスが指定されていない場合は、HTMLと同じディレクトリに.pdfフォルダを作成
    if len(sys.argv) >= 3:
        pdf_path = sys.argv[2]
    else:
        html_dir = os.path.dirname(html_path)
        html_name = os.path.splitext(os.path.basename(html_path))[0]
        pdf_dir = os.path.join(html_dir, '.pdf')
        os.makedirs(pdf_dir, exist_ok=True)
        pdf_path = os.path.join(pdf_dir, f"{html_name}.pdf")
    
    # HTMLファイルの存在確認
    if not os.path.exists(html_path):
        print(f"エラー: HTMLファイルが見つかりません: {html_path}")
        sys.exit(1)
    
    # 変換実行
    html_to_pdf(html_path, pdf_path)


if __name__ == "__main__":
    main()