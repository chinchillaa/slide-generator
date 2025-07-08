#!/usr/bin/env python3
"""
HTMLスライドを分割してPDFに変換するツール（WSL対応版）
各スライドを個別のHTMLファイルに分割し、pdfkitで変換後に結合
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
import subprocess

# 必要なライブラリのインポート
try:
    import pdfkit
except ImportError:
    print("pdfkitがインストールされていません。")
    print("uv pip install pdfkit")
    sys.exit(1)

try:
    from pypdf import PdfWriter, PdfReader
except ImportError:
    print("pypdfがインストールされていません。")
    print("uv pip install pypdf")
    sys.exit(1)


def check_wkhtmltopdf():
    """wkhtmltopdfがインストールされているか確認"""
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"wkhtmltopdf が見つかりました: {result.stdout.split()[1]}")
            return True
    except FileNotFoundError:
        pass
    
    print("エラー: wkhtmltopdfがインストールされていません。")
    print("インストール方法:")
    print("  sudo apt-get update")
    print("  sudo apt-get install wkhtmltopdf")
    return False


def extract_slides_to_individual_html(html_file_path, temp_dir):
    """
    HTMLファイルから各スライドを個別のHTMLファイルとして抽出
    
    Args:
        html_file_path: 入力HTMLファイルのパス
        temp_dir: 一時ファイルを保存するディレクトリ
        
    Returns:
        生成されたHTMLファイルのパスリスト
    """
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 元のHTMLのヘッド部分を取得
    head_content = soup.find('head')
    if not head_content:
        print("エラー: HTMLにheadタグが見つかりません")
        return []
    
    # スタイルとリンクを保持
    styles = []
    for style in soup.find_all('style'):
        styles.append(str(style))
    
    css_links = []
    for link in soup.find_all('link', rel='stylesheet'):
        css_links.append(str(link))
    
    # Font Awesomeのリンクを確実に含める
    if not any('fontawesome' in str(link) for link in css_links):
        css_links.append('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">')
    
    # スライドコンテナを取得
    slides = soup.find_all('div', class_='slide-container')
    
    if not slides:
        print("エラー: スライドが見つかりません")
        return []
    
    html_files = []
    
    for i, slide in enumerate(slides, 1):
        # 各スライド用のHTMLを作成
        slide_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide {i}</title>
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
            background-color: white;
            width: 1280px;
            height: 720px;
            overflow: hidden;
        }}
        
        /* スライドコンテナの強制表示 */
        .slide-container {{
            width: 1280px !important;
            height: 720px !important;
            background-color: white !important;
            position: relative !important;
            overflow: hidden !important;
            display: block !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        
        /* ナビゲーションを非表示 */
        .navigation {{
            display: none !important;
        }}
        
        /* PDFのページ設定 */
        @page {{
            size: 1280px 720px;
            margin: 0;
        }}
        
        /* 印刷時の設定 */
        @media print {{
            body {{
                width: 1280px;
                height: 720px;
                margin: 0;
                padding: 0;
            }}
            .slide-container {{
                page-break-after: avoid;
                page-break-inside: avoid;
            }}
        }}
    </style>
    {''.join(styles)}
</head>
<body>
    {str(slide)}
</body>
</html>"""
        
        # HTMLファイルを保存
        html_file_path = os.path.join(temp_dir, f'slide_{i:02d}.html')
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(slide_html)
        
        html_files.append(html_file_path)
        print(f"スライド {i} を抽出: {html_file_path}")
    
    return html_files


def convert_html_to_pdf(html_file, pdf_file):
    """
    個別のHTMLファイルをPDFに変換
    
    Args:
        html_file: 入力HTMLファイルのパス
        pdf_file: 出力PDFファイルのパス
    """
    options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None,
        'print-media-type': None,
        'disable-smart-shrinking': None,
        'zoom': 0.75,  # スケーリング調整
        'dpi': 150,    # 高解像度
        'quiet': None
    }
    
    try:
        pdfkit.from_file(html_file, pdf_file, options=options)
        return True
    except Exception as e:
        print(f"エラー: {html_file} の変換に失敗: {e}")
        return False


def merge_pdfs(pdf_files, output_pdf_path):
    """
    複数のPDFファイルを1つに結合
    
    Args:
        pdf_files: 結合するPDFファイルのリスト
        output_pdf_path: 出力PDFファイルのパス
    """
    writer = PdfWriter()
    
    for pdf_file in pdf_files:
        try:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                writer.add_page(page)
        except Exception as e:
            print(f"警告: {pdf_file} の読み込みに失敗: {e}")
    
    with open(output_pdf_path, 'wb') as output_file:
        writer.write(output_file)


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_split_and_convert.py <HTMLファイル> [出力PDFファイル]")
        sys.exit(1)
    
    # wkhtmltopdfの確認
    if not check_wkhtmltopdf():
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
    
    # 一時ディレクトリの作成
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"作業ディレクトリ: {temp_dir}")
        
        # スライドを個別のHTMLファイルに分割
        print("\n1. HTMLスライドを分割中...")
        html_files = extract_slides_to_individual_html(html_file, temp_dir)
        
        if not html_files:
            print("エラー: 分割できるスライドがありません")
            sys.exit(1)
        
        # 各HTMLをPDFに変換
        print(f"\n2. {len(html_files)} 個のスライドをPDFに変換中...")
        pdf_files = []
        
        for i, html_file_path in enumerate(html_files, 1):
            pdf_file_path = html_file_path.replace('.html', '.pdf')
            print(f"   変換中 {i}/{len(html_files)}: {os.path.basename(html_file_path)}")
            
            if convert_html_to_pdf(html_file_path, pdf_file_path):
                pdf_files.append(pdf_file_path)
            else:
                print(f"   警告: {html_file_path} の変換をスキップ")
        
        if not pdf_files:
            print("エラー: PDFに変換できたスライドがありません")
            sys.exit(1)
        
        # PDFを結合
        print(f"\n3. {len(pdf_files)} 個のPDFを結合中...")
        merge_pdfs(pdf_files, output_pdf)
        
        print(f"\n✅ PDFが正常に生成されました: {output_pdf}")
        print(f"   ページ数: {len(pdf_files)}")


if __name__ == "__main__":
    main()