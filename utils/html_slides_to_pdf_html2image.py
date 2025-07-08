#!/usr/bin/env python3
"""
HTMLスライドをPDFに変換するツール（html2image版）
WSL環境でも動作する軽量なアプローチ
"""

import os
import sys
import tempfile
from pathlib import Path
from PIL import Image
from bs4 import BeautifulSoup
import base64
import io
import re

try:
    from html2image import Html2Image
except ImportError:
    print("html2imageがインストールされていません。")
    print("uv pip install html2image")
    sys.exit(1)


def extract_slides_and_create_images(html_file_path, temp_dir):
    """
    HTMLファイルから各スライドを抽出して画像化
    
    Args:
        html_file_path: 入力HTMLファイルのパス
        temp_dir: 一時ファイルを保存するディレクトリ
        
    Returns:
        生成された画像ファイルのパスリスト
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
    
    # スライドコンテナを取得
    slides = soup.find_all('div', class_='slide-container')
    
    if not slides:
        print("エラー: スライドが見つかりません")
        return []
    
    # html2imageの初期化
    hti = Html2Image(
        output_path=temp_dir,
        size=(1280, 720),  # スライドサイズ
        custom_flags=['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
    )
    
    image_files = []
    
    for i, slide in enumerate(slides, 1):
        print(f"スライド {i}/{len(slides)} を処理中...")
        
        # 各スライド用のHTMLを作成
        slide_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide {i}</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.0/css/all.min.css">
    <style>
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
        
        .navigation {{
            display: none !important;
        }}
        
        /* 緑色のスタイル */
        .green-accent {{
            background-color: #22c55e;
        }}
        
        .highlight-text {{
            color: #22c55e;
            font-weight: bold;
        }}
        
        .icon-circle {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: rgba(34, 197, 94, 0.15);
            display: flex;
            align-items: center;
            justify-content: center;
        }}
    </style>
    {''.join(styles)}
</head>
<body>
    {str(slide)}
</body>
</html>"""
        
        # 画像として保存
        image_name = f'slide_{i:02d}.png'
        
        try:
            # HTMLを画像に変換
            hti.screenshot(html_str=slide_html, save_as=image_name)
            image_path = os.path.join(temp_dir, image_name)
            
            if os.path.exists(image_path):
                image_files.append(image_path)
                print(f"  ✓ 画像を生成: {image_name}")
            else:
                print(f"  ✗ 画像の生成に失敗: {image_name}")
                
        except Exception as e:
            print(f"  エラー: {e}")
    
    return image_files


def images_to_pdf(image_files, output_pdf_path):
    """
    画像ファイルをPDFに変換
    
    Args:
        image_files: 画像ファイルのパスリスト
        output_pdf_path: 出力PDFファイルのパス
    """
    if not image_files:
        print("エラー: 変換する画像がありません")
        return False
    
    try:
        # 画像を開く
        images = []
        for img_path in image_files:
            img = Image.open(img_path)
            # RGBに変換（PDFはRGBAをサポートしない）
            if img.mode == 'RGBA':
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3])
                images.append(rgb_img)
            else:
                images.append(img)
        
        # PDFとして保存
        if len(images) > 1:
            images[0].save(
                output_pdf_path,
                'PDF',
                save_all=True,
                append_images=images[1:],
                resolution=150.0,
                quality=95
            )
        else:
            images[0].save(
                output_pdf_path,
                'PDF',
                resolution=150.0,
                quality=95
            )
        
        print(f"✅ PDFが正常に生成されました: {output_pdf_path}")
        return True
        
    except Exception as e:
        print(f"エラー: PDF生成に失敗: {e}")
        return False


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_to_pdf_html2image.py <HTMLファイル> [出力PDFファイル]")
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
    
    # 一時ディレクトリで作業
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"作業ディレクトリ: {temp_dir}")
        
        # スライドを画像に変換
        print("\n1. HTMLスライドを画像に変換中...")
        image_files = extract_slides_and_create_images(html_file, temp_dir)
        
        if not image_files:
            print("エラー: 変換できた画像がありません")
            sys.exit(1)
        
        print(f"\n2. {len(image_files)} 個の画像をPDFに結合中...")
        success = images_to_pdf(image_files, output_pdf)
        
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()