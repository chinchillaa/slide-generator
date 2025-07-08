# Deep Research Slides Generator

AIを使って詳細な調査を行い、美しいプレゼンテーションスライドを自動生成するWebアプリケーションです。

## 機能

- 🔍 **Deep Research**: Hugging FaceのsmolagentsとOpenAIのDeep Research手法を使用した高度な調査
- 🎨 **美しいスライドデザイン**: SB C&Sのブランドガイドラインに準拠したプロフェッショナルなデザイン
- 🚀 **リアルタイム進捗表示**: WebSocketを使用した調査進捗のリアルタイム更新
- 📥 **スライドダウンロード**: 生成されたスライドをHTMLファイルとしてダウンロード可能

## 技術スタック

### バックエンド
- FastAPI
- smolagents (Hugging Face)
- WebSocket
- Jinja2 (テンプレートエンジン)

### フロントエンド
- React + TypeScript
- Vite
- Tailwind CSS
- Axios

## セットアップ

### 1. リポジトリのクローン

```bash
cd /home/chinchilla/work/slide_generator/deep_research_slides
```

### 2. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# smolagentsのインストール
pip install -e ../../smolagents/[dev]

# 環境変数の設定
cp .env.example .env
# .envファイルを編集して、必要なAPIキーを設定
```

### 3. フロントエンドのセットアップ

```bash
cd ../frontend

# 依存関係のインストール
npm install
```

## 実行方法

### バックエンドの起動

```bash
cd backend
python run.py
```

バックエンドは `http://localhost:8000` で起動します。

### フロントエンドの起動

```bash
cd frontend
npm run dev
```

フロントエンドは `http://localhost:3000` で起動します。

## 使い方

1. ブラウザで `http://localhost:3000` にアクセス
2. 調査したいトピックを入力
3. 使用するAIモデルと最大スライド数を選択
4. 「調査を開始」ボタンをクリック
5. リアルタイムで進捗を確認
6. 完了後、生成されたスライドをプレビューまたはダウンロード

## APIエンドポイント

- `POST /research`: 新しい調査リクエストを作成
- `WS /ws`: WebSocket接続（進捗更新用）
- `GET /health`: ヘルスチェック

## スライドデザイン

生成されるスライドは以下の要素を含みます：

- タイトルページ
- 概要
- 主要な事実
- 重要な洞察
- 統計データ
- まとめと情報源

デザインは緑色（#22c55e）をメインカラーとし、SB C&Sのロゴが各スライドに配置されます。

## 環境変数

`.env`ファイルに以下の環境変数を設定してください：

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
HF_TOKEN=your_huggingface_token

# Search API Keys (いずれか1つ)
SERPAPI_API_KEY=your_serpapi_key
SERPER_API_KEY=your_serper_key

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## トラブルシューティング

### smolagentsが見つからない場合

```bash
# smolagentsのパスを確認
ls ../../smolagents/

# 存在しない場合は、smolagentsをクローン
cd ../..
git clone https://github.com/huggingface/smolagents.git
```

### APIキーエラー

- `.env`ファイルが正しく設定されているか確認
- 必要なAPIキーが有効か確認

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。