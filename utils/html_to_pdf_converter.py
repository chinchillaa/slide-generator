#!/usr/bin/env python3
"""
HTMLスライドをPDFに変換するツール
Playwrightを使用してHTMLファイルをPDFに変換します
"""

import asyncio
import os
import sys
from pathlib import Path

# Playwrightのインポートを試みる
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwrightがインストールされていません。")
    print("以下のコマンドでインストールしてください：")
    print("pip install playwright")
    print("playwright install chromium")
    sys.exit(1)


async def html_to_pdf(html_path: str, pdf_path: str):
    """
    HTMLファイルをPDFに変換
    
    Args:
        html_path: 入力HTMLファイルのパス
        pdf_path: 出力PDFファイルのパス
    """
    async with async_playwright() as p:
        # ブラウザを起動
        browser = await p.chromium.launch(headless=True)
        
        try:
            # 新しいページを作成
            page = await browser.new_page()
            
            # HTMLファイルを開く
            file_url = f"file://{os.path.abspath(html_path)}"
            await page.goto(file_url)
            
            # ページが完全に読み込まれるまで待機
            await page.wait_for_load_state('networkidle')
            
            # JavaScriptでスライドの総数を取得
            total_slides = await page.evaluate('''
                () => {
                    // グローバル変数totalSlidesを返す
                    return window.totalSlides || document.querySelectorAll('.slide-container').length;
                }
            ''')
            
            print(f"総スライド数: {total_slides}")
            
            # 各スライドを表示してPDFページを作成
            pdf_pages = []
            
            for slide_num in range(1, total_slides + 1):
                print(f"スライド {slide_num}/{total_slides} を処理中...")
                
                # JavaScriptでスライドを切り替え
                await page.evaluate(f'''
                    () => {{
                        // すべてのスライドを非表示
                        document.querySelectorAll('.slide-container').forEach(slide => {{
                            slide.classList.remove('active');
                        }});
                        
                        // 指定されたスライドを表示
                        const targetSlide = document.getElementById('slide-{slide_num}');
                        if (targetSlide) {{
                            targetSlide.classList.add('active');
                        }}
                    }}
                ''')
                
                # スライドが表示されるまで待機
                await page.wait_for_timeout(500)
                
                # スライドをPDFとして保存（一時ファイル）
                temp_pdf = f"/tmp/slide_{slide_num}.pdf"
                await page.pdf(
                    path=temp_pdf,
                    format='A4',
                    landscape=True,
                    print_background=True,
                    margin={
                        'top': '0px',
                        'bottom': '0px',
                        'left': '0px',
                        'right': '0px'
                    }
                )
                pdf_pages.append(temp_pdf)
            
            # PDFページを結合（PyPDF2が必要）
            try:
                from PyPDF2 import PdfMerger
                
                merger = PdfMerger()
                for pdf_page in pdf_pages:
                    merger.append(pdf_page)
                
                # 最終的なPDFを保存
                merger.write(pdf_path)
                merger.close()
                
                # 一時ファイルを削除
                for pdf_page in pdf_pages:
                    os.remove(pdf_page)
                    
                print(f"PDFを保存しました: {pdf_path}")
                
            except ImportError:
                # PyPDF2がない場合は単一ページのPDFとして保存
                print("PyPDF2がインストールされていないため、最初のページのみPDFとして保存します。")
                
                # すべてのスライドを表示
                await page.evaluate('''
                    () => {
                        document.querySelectorAll('.slide-container').forEach(slide => {
                            slide.classList.add('active');
                            slide.style.pageBreakAfter = 'always';
                            slide.style.marginBottom = '20px';
                        });
                    }
                ''')
                
                await page.wait_for_timeout(1000)
                
                # すべてのスライドを含むPDFを生成
                await page.pdf(
                    path=pdf_path,
                    format='A4',
                    landscape=True,
                    print_background=True,
                    margin={
                        'top': '10px',
                        'bottom': '10px',
                        'left': '10px',
                        'right': '10px'
                    }
                )
                
                print(f"PDFを保存しました: {pdf_path}")
        
        finally:
            await browser.close()


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_to_pdf_converter.py <HTMLファイルパス> [PDFファイルパス]")
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
    
    # 非同期関数を実行
    asyncio.run(html_to_pdf(html_path, pdf_path))


if __name__ == "__main__":
    main()