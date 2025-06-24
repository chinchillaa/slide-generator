# HTML to PPTX Converter

HTMLファイルをPowerPoint (PPTX)形式に変換する汎用的なPythonモジュールです。

## 特徴

- HTMLスライドコンテンツの解析
- PowerPointプレゼンテーションの生成
- python-pptxライブラリまたはネイティブXML生成のサポート
- 日本語フォントのサポート
- Tailwindクラスのスタイル解析

## インストール

### 基本インストール（ネイティブXML生成のみ）
```bash
# 追加のパッケージは不要です
```

### python-pptxを使用する場合
```bash
pip install python-pptx
```

## 使用方法

### コマンドライン

```bash
# 基本的な使用方法
python -m html_to_pptx.cli input.html

# 出力ファイル名を指定
python -m html_to_pptx.cli input.html output.pptx

# ネイティブXML生成を強制
python -m html_to_pptx.cli input.html --native
```

### Pythonコード

```python
from html_to_pptx import HTMLtoPPTXConverter

# コンバーターの初期化
converter = HTMLtoPPTXConverter()

# HTMLファイルを変換
converter.convert_file('input.html', 'output.pptx')

# HTML文字列を変換
html_content = '<html>...</html>'
converter.convert_string(html_content, 'output.pptx')
```

## モジュール構成

```
html_to_pptx/
├── __init__.py          # パッケージ初期化
├── __main__.py          # スクリプト実行用
├── cli.py               # コマンドラインインターフェース
├── core/
│   ├── __init__.py
│   └── converter.py     # メインコンバータークラス
├── parsers/
│   ├── __init__.py
│   └── html_parser.py   # HTMLパーサー
├── builders/
│   ├── __init__.py
│   └── pptx_builder.py  # PPTXビルダー
└── utils/
    ├── __init__.py
    └── xml_templates.py # XMLテンプレート
```

## サポートされるHTMLフォーマット

このコンバーターは以下のHTML構造をサポートします：

- `.slide-container` クラスを持つdiv要素
- `<h1>` タグ（タイトル）
- `<h2>` タグ（サブタイトル）
- `.subtitle` クラスを持つdiv要素（期間情報など）
- Tailwindクラスによるスタイリング

## 制限事項

- 現在は基本的なテキストスライドのみサポート
- 画像、グラフ、表などの複雑な要素は未サポート
- アニメーションは未サポート

## 今後の拡張予定

- 画像のサポート
- グラフ・表のサポート
- 複数スライドのサポート
- カスタムレイアウトのサポート
- より高度なスタイリングオプション