#!/usr/bin/env python3
"""
HTMLスライドをPDFに変換するツール（Selenium版）
複数のスライドを含むHTMLファイルを高品質なPDFに変換する
"""

import os
import sys
import time
from pathlib import Path
from PIL import Image
import io

# Seleniumのインポート
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.chrome.service import Service
except ImportError:
    print("Seleniumがインストールされていません。")
    print("uv pip install selenium pillow")
    sys.exit(1)


def setup_driver():
    """
    Chromeドライバーをヘッドレスモードで設定
    """
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    
    # 高品質スクリーンショットのための設定
    options.add_argument('--force-device-scale-factor=2')  # 2倍の解像度
    options.add_argument('--window-size=2560,1440')  # 大きめのウィンドウサイズ
    
    # 日本語フォントの設定
    options.add_argument('--lang=ja')
    
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Chrome WebDriverの初期化に失敗しました: {e}")
        print("\nChrome WebDriverが必要です。以下の方法でインストールしてください：")
        print("1. Google Chromeをインストール")
        print("2. chromedriverをダウンロードしてPATHに追加")
        print("   または")
        print("3. uv pip install webdriver-manager")
        return None


def capture_slides_with_selenium(html_file_path, output_pdf_path):
    """
    SeleniumでHTMLファイルの各スライドをキャプチャしてPDFに変換
    
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
    
    # WebDriverの設定
    driver = setup_driver()
    if not driver:
        # webdriver-managerを試す
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            service = Service(ChromeDriverManager().install())
            options = ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--force-device-scale-factor=2')
            options.add_argument('--window-size=2560,1440')
            options.add_argument('--lang=ja')
            
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"webdriver-managerでも失敗しました: {e}")
            return False
    
    try:
        # HTMLファイルを開く
        file_url = f"file://{html_file_path}"
        print(f"HTMLファイルを開いています: {file_url}")
        driver.get(file_url)
        
        # ページの読み込みを待つ
        time.sleep(2)
        
        # JavaScriptで実際のスライドサイズを1280x720に設定
        driver.execute_script("""
            // ビューポートを調整
            document.body.style.margin = '0';
            document.body.style.padding = '0';
            document.body.style.overflow = 'hidden';
        """)
        
        # スライドの総数を取得
        slide_count = driver.execute_script("""
            return document.querySelectorAll('.slide-container').length;
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
            driver.execute_script(f"""
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
                    
                    // スライドのサイズを確実に設定
                    currentSlide.style.width = '1280px';
                    currentSlide.style.height = '720px';
                    currentSlide.style.position = 'relative';
                }}
                
                // ナビゲーションを非表示
                const nav = document.querySelector('.navigation');
                if (nav) {{
                    nav.style.display = 'none';
                }}
            """)
            
            # 少し待機
            time.sleep(1)
            
            # スライド要素を取得
            slide_element = driver.find_element(By.ID, f'slide-{i}')
            
            # スライドの位置とサイズを取得
            location = slide_element.location
            size = slide_element.size
            
            # ページ全体のスクリーンショットを取得
            screenshot_bytes = driver.get_screenshot_as_png()
            
            # PIL Imageオブジェクトに変換
            full_image = Image.open(io.BytesIO(screenshot_bytes))
            
            # スライド部分を切り出し（2倍の解像度を考慮）
            scale_factor = 2  # force-device-scale-factor=2
            left = int(location['x'] * scale_factor)
            top = int(location['y'] * scale_factor)
            right = left + int(1280 * scale_factor)
            bottom = top + int(720 * scale_factor)
            
            # 切り出し
            slide_image = full_image.crop((left, top, right, bottom))
            
            # 元のサイズ（1280x720）にリサイズ（高品質）
            slide_image = slide_image.resize((1280, 720), Image.Resampling.LANCZOS)
            
            images.append(slide_image)
        
        # PDFとして保存
        if images:
            print(f"PDFを生成中: {output_pdf_path}")
            
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
                    resolution=150.0,  # 高解像度
                    quality=95  # 高品質
                )
            else:
                rgb_images[0].save(
                    output_pdf_path, 
                    'PDF', 
                    resolution=150.0,
                    quality=95
                )
            
            print(f"✅ PDFが正常に生成されました: {output_pdf_path}")
            return True
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        driver.quit()


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_to_pdf_selenium.py <HTMLファイル> [出力PDFファイル]")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    # 出力ファイル名の決定
    if len(sys.argv) >= 3:
        output_pdf = sys.argv[2]
    else:
        # 入力ファイルと同じディレクトリに、拡張子を.pdfに変えて保存
        output_pdf = Path(html_file).with_suffix('.pdf')
    
    # 変換を実行
    success = capture_slides_with_selenium(html_file, output_pdf)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()