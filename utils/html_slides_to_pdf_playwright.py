#!/usr/bin/env python3
"""
HTMLスライドをPDFに変換するツール（Playwright版）
複数のスライドを含むHTMLファイルを各スライドごとにキャプチャし、PDFに結合する
"""

import asyncio
import os
import sys
from pathlib import Path
from PIL import Image
import io

# Playwrightのインポート
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("Playwrightがインストールされていません。")
    print("pip install playwright")
    print("playwright install chromium")
    sys.exit(1)


async def capture_slides_to_pdf(html_file_path, output_pdf_path):
    """
    HTMLファイルの各スライドをキャプチャしてPDFに変換
    
    Args:
        html_file_path: 入力HTMLファイルのパス
        output_pdf_path: 出力PDFファイルのパス
    """
    # 絶対パスに変換
    html_file_path = Path(html_file_path).absolute()
    output_pdf_path = Path(output_pdf_path).absolute()
    
    if not html_file_path.exists():
        print(f"エラー: HTMLファイルが見つかりません: {html_file_path}")
        return False
    
    # 出力ディレクトリの作成
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        # ブラウザを起動（ヘッドレスモード）
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            device_scale_factor=2  # 高解像度でキャプチャ
        )
        page = await context.new_page()
        
        try:
            # HTMLファイルを開く
            file_url = f"file://{html_file_path}"
            print(f"HTMLファイルを開いています: {file_url}")
            await page.goto(file_url)
            
            # ページの読み込みを待つ
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)  # 追加の待機時間
            
            # スライドの総数を取得
            slide_count = await page.evaluate("""
                () => {
                    const slides = document.querySelectorAll('.slide-container');
                    return slides.length;
                }
            """)
            
            print(f"検出されたスライド数: {slide_count}")
            
            if slide_count == 0:
                print("エラー: スライドが見つかりません")
                return False
            
            images = []
            
            # 各スライドをキャプチャ
            for i in range(1, slide_count + 1):
                print(f"スライド {i}/{slide_count} をキャプチャ中...")
                
                # すべてのスライドを非表示にして、現在のスライドのみ表示
                await page.evaluate(f"""
                    () => {{
                        // すべてのスライドを非表示
                        document.querySelectorAll('.slide-container').forEach(slide => {{
                            slide.classList.remove('active');
                            slide.style.display = 'none';
                        }});
                        
                        // 現在のスライドを表示
                        const currentSlide = document.getElementById('slide-{i}');
                        if (currentSlide) {{
                            currentSlide.classList.add('active');
                            currentSlide.style.display = 'block';
                        }}
                    }}
                """)
                
                # 少し待機
                await asyncio.sleep(0.5)
                
                # スライドのスクリーンショットを取得
                screenshot_bytes = await page.locator(f'#slide-{i}').screenshot(
                    type='png',
                    full_page=False
                )
                
                # PIL Imageオブジェクトに変換
                image = Image.open(io.BytesIO(screenshot_bytes))
                images.append(image)
            
            # PDFとして保存
            if images:
                print(f"PDFを生成中: {output_pdf_path}")
                
                # 最初の画像をベースにPDFを作成
                first_image = images[0]
                
                # RGBモードに変換（PDFはRGBAをサポートしない）
                rgb_images = []
                for img in images:
                    if img.mode == 'RGBA':
                        rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                        rgb_img.paste(img, mask=img.split()[3])
                        rgb_images.append(rgb_img)
                    else:
                        rgb_images.append(img)
                
                # PDFとして保存
                if len(rgb_images) > 1:
                    rgb_images[0].save(
                        output_pdf_path,
                        'PDF',
                        save_all=True,
                        append_images=rgb_images[1:],
                        resolution=100.0
                    )
                else:
                    rgb_images[0].save(output_pdf_path, 'PDF', resolution=100.0)
                
                print(f"✅ PDFが正常に生成されました: {output_pdf_path}")
                return True
            
        except Exception as e:
            print(f"エラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        finally:
            await browser.close()


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_to_pdf_playwright.py <HTMLファイル> [出力PDFファイル]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    # 出力ファイル名の決定
    if len(sys.argv) >= 3:
        output_pdf = sys.argv[2]
    else:
        # 入力ファイルと同じディレクトリに、拡張子を.pdfに変えて保存
        output_pdf = Path(html_file).with_suffix('.pdf')
    
    # 非同期関数を実行
    success = asyncio.run(capture_slides_to_pdf(html_file, output_pdf))
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()