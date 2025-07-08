#!/usr/bin/env python3
"""
HTMLスライドをPDFに変換するツール（weasyprint版）
複数のスライドを含むHTMLファイルを処理してPDFに変換する
"""

import os
import sys
from pathlib import Path
from bs4 import BeautifulSoup
import re

# weasyprintのインポート
try:
    import weasyprint
    from weasyprint import HTML, CSS
except ImportError:
    print("weasyprintがインストールされていません。")
    print("uv pip install weasyprint beautifulsoup4")
    sys.exit(1)


def extract_and_process_slides(html_file_path):
    """
    HTMLファイルから各スライドを抽出して処理
    
    Args:
        html_file_path: 入力HTMLファイルのパス
        
    Returns:
        処理済みのHTML文字列のリスト
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # スタイルタグを取得
    styles = []
    for style in soup.find_all('style'):
        styles.append(str(style))
    
    # 外部スタイルシートのリンクを取得
    css_links = []
    for link in soup.find_all('link', rel='stylesheet'):
        css_links.append(str(link))
    
    # スライドコンテナを取得
    slides = soup.find_all('div', class_='slide-container')
    
    if not slides:
        print("エラー: スライドが見つかりません")
        return []
    
    processed_slides = []
    
    for i, slide in enumerate(slides, 1):
        # 各スライドを個別のHTMLドキュメントとして作成
        slide_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide {i}</title>
    {''.join(css_links)}
    <style>
        @page {{
            size: 1280px 720px;
            margin: 0;
        }}
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Hiragino Sans', 'Meiryo', sans-serif;
            background-color: white;
        }}
        .slide-container {{
            width: 1280px;
            height: 720px;
            background-color: white;
            position: relative;
            overflow: hidden;
            display: block !important;
        }}
        /* ナビゲーションを非表示 */
        .navigation {{
            display: none !important;
        }}
    </style>
    {''.join(styles)}
</head>
<body>
    {str(slide)}
</body>
</html>"""
        
        # slide-containerのdisplay: noneを強制的に上書き
        slide_html = slide_html.replace('display: none;', 'display: block !important;')
        
        processed_slides.append(slide_html)
    
    return processed_slides


def create_combined_pdf(html_slides, output_pdf_path):
    """
    複数のHTMLスライドを結合してPDFを作成
    
    Args:
        html_slides: HTMLスライドのリスト
        output_pdf_path: 出力PDFファイルのパス
    """
    if not html_slides:
        print("エラー: 変換するスライドがありません")
        return False
    
    try:
        # 一時的なPDFファイルを作成
        temp_pdfs = []
        
        for i, slide_html in enumerate(html_slides, 1):
            print(f"スライド {i}/{len(html_slides)} を変換中...")
            
            # HTMLをPDFに変換
            pdf_bytes = HTML(string=slide_html).write_pdf()
            temp_pdfs.append(pdf_bytes)
        
        # PyPDF2を使用してPDFを結合
        try:
            from pypdf import PdfWriter, PdfReader
            import io
            
            writer = PdfWriter()
            
            for pdf_bytes in temp_pdfs:
                reader = PdfReader(io.BytesIO(pdf_bytes))
                for page in reader.pages:
                    writer.add_page(page)
            
            # 結合したPDFを保存
            with open(output_pdf_path, 'wb') as f:
                writer.write(f)
                
        except ImportError:
            # PyPDF2がない場合は最初のページのみ保存
            print("警告: PyPDF2がインストールされていないため、最初のページのみ保存します")
            print("全ページを保存するには: uv pip install pypdf")
            with open(output_pdf_path, 'wb') as f:
                f.write(temp_pdfs[0])
        
        print(f"✅ PDFが正常に生成されました: {output_pdf_path}")
        return True
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_to_pdf_weasyprint.py <HTMLファイル> [出力PDFファイル]")
        sys.exit(1)
    
    html_file = Path(sys.argv[1]).absolute()
    
    # 出力ファイル名の決定
    if len(sys.argv) >= 3:
        output_pdf = Path(sys.argv[2]).absolute()
    else:
        output_pdf = html_file.with_suffix('.pdf')
    
    if not html_file.exists():
        print(f"エラー: HTMLファイルが見つかりません: {html_file}")
        sys.exit(1)
    
    # 出力ディレクトリの作成
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"HTMLファイルを読み込んでいます: {html_file}")
    
    # スライドを抽出して処理
    html_slides = extract_and_process_slides(html_file)
    
    if not html_slides:
        print("エラー: 処理可能なスライドが見つかりません")
        sys.exit(1)
    
    print(f"検出されたスライド数: {len(html_slides)}")
    
    # PDFを作成
    success = create_combined_pdf(html_slides, output_pdf)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()