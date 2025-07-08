#!/usr/bin/env python3
"""
HTMLスライドをPDFに変換するツール
WeasyPrintを使用してHTMLファイルをPDFに変換します
"""

import os
import sys
from pathlib import Path
from weasyprint import HTML, CSS
from PyPDF2 import PdfMerger, PdfReader
import tempfile
import re


def extract_slides_from_html(html_content):
    """
    HTMLからスライドコンテナを抽出し、個別のHTMLとして返す
    """
    # 基本的なHTML構造を抽出
    head_match = re.search(r'<head>(.*?)</head>', html_content, re.DOTALL)
    head_content = head_match.group(1) if head_match else ''
    
    # スタイルタグを抽出
    style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    style_content = style_match.group(1) if style_match else ''
    
    # 各スライドコンテナを抽出
    slide_pattern = r'<div class="slide-container.*?" id="slide-(\d+)".*?>(.*?)</div>\s*(?=<div class="slide-container|<!-- ナビゲーション|<!-- スライド|$)'
    slides = re.findall(slide_pattern, html_content, re.DOTALL)
    
    slide_htmls = []
    for slide_num, slide_content in slides:
        # 各スライド用のHTMLを作成
        slide_html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
{head_content}
<style>
{style_content}
/* PDF用の追加スタイル */
body {{
    margin: 0;
    padding: 0;
    width: 1280px;
    height: 720px;
}}
.slide-container {{
    display: block !important;
    page-break-after: always;
    width: 1280px;
    height: 720px;
    margin: 0;
}}
.navigation {{
    display: none !important;
}}
</style>
</head>
<body>
    <div class="slide-container active" id="slide-{slide_num}">
{slide_content}
    </div>
</body>
</html>
"""
        slide_htmls.append((slide_num, slide_html))
    
    return slide_htmls


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
    
    # スライドを抽出
    slides = extract_slides_from_html(html_content)
    print(f"見つかったスライド数: {len(slides)}")
    
    if not slides:
        print("エラー: スライドが見つかりませんでした")
        return
    
    # 一時PDFファイルを作成
    temp_pdfs = []
    
    for slide_num, slide_html in slides:
        print(f"スライド {slide_num} を処理中...")
        
        # 一時HTMLファイルを作成
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as tmp_html:
            tmp_html.write(slide_html)
            tmp_html_path = tmp_html.name
        
        # 一時PDFファイルパス
        tmp_pdf_path = tempfile.mktemp(suffix='.pdf')
        
        try:
            # HTMLをPDFに変換
            # CSS for A4 landscape
            css = CSS(string='''
                @page {
                    size: A4 landscape;
                    margin: 0;
                }
            ''')
            
            # WeasyPrintでPDFを生成
            HTML(filename=tmp_html_path).write_pdf(
                tmp_pdf_path,
                stylesheets=[css]
            )
            
            temp_pdfs.append(tmp_pdf_path)
            
        except Exception as e:
            print(f"スライド {slide_num} の変換中にエラーが発生しました: {e}")
        
        finally:
            # 一時HTMLファイルを削除
            os.unlink(tmp_html_path)
    
    # PDFを結合
    if temp_pdfs:
        print("PDFを結合中...")
        merger = PdfMerger()
        
        for pdf_path in temp_pdfs:
            try:
                merger.append(pdf_path)
            except Exception as e:
                print(f"PDF結合中にエラーが発生しました: {e}")
        
        # 最終的なPDFを保存
        with open(pdf_path, 'wb') as output_file:
            merger.write(output_file)
        merger.close()
        
        # 一時PDFファイルを削除
        for pdf_path in temp_pdfs:
            try:
                os.unlink(pdf_path)
            except:
                pass
        
        print(f"PDFを保存しました: {pdf_path}")
    else:
        print("エラー: 変換できたスライドがありませんでした")


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法: python html_slides_to_pdf.py <HTMLファイルパス> [PDFファイルパス]")
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