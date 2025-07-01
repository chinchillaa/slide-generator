# Deep Research Slides Generator - クイックスタートガイド

## 前提条件

- Python 3.8以上
- Node.js 16以上
- 以下のAPIキー:
  - OpenAI API Key (GPT-4oアクセス権限付き)
  - Hugging Face Token
  - Serper API Key または SerpAPI Key

## 1. APIキーの取得

### OpenAI API Key
1. https://platform.openai.com/api-keys にアクセス
2. "Create new secret key"をクリック
3. キーをコピー

### Hugging Face Token
1. https://huggingface.co/settings/tokens にアクセス
2. "New token"をクリック
3. 以下のパーミッションを選択:
   - Read access to contents of all public gated repos you can access
   - Make calls to Inference Providers
4. "Generate token"をクリック

### Serper API Key
1. https://serper.dev/signup でアカウント作成
2. ダッシュボードからAPIキーを取得

## 2. 環境設定

```bash
# バックエンドディレクトリに移動
cd /home/chinchilla/work/slide_generator/deep_research_slides/backend

# .envファイルを編集
nano .env
# または
vim .env
```

以下のように設定:
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxx
HF_TOKEN=hf_xxxxxxxxxxxx
SERPER_API_KEY=xxxxxxxxxxxx
```

## 3. 依存関係のインストール

### バックエンド
```bash
cd backend
pip3 install -r requirements.txt

# smolagentsのインストール
cd ../..
pip3 install -e ./smolagents/
```

### フロントエンド
```bash
cd deep_research_slides/frontend
npm install
```

## 4. アプリケーションの起動

### ターミナル1: バックエンド
```bash
cd backend
python3 run.py
```

### ターミナル2: フロントエンド
```bash
cd frontend
npm run dev
```

## 5. 使用方法

1. ブラウザで http://localhost:3000 を開く
2. 調査したいトピックを入力（例: "日本の電気自動車市場の現状と将来展望"）
3. モデルを選択（推奨: GPT-4o）
4. "調査を開始"をクリック
5. 進捗バーで調査状況を確認
6. 完了後、スライドをプレビューまたはダウンロード

## トラブルシューティング

### "Module not found"エラー
```bash
# すべての依存関係を再インストール
pip3 install --upgrade -r requirements.txt
```

### WebSocket接続エラー
- バックエンドが起動しているか確認
- ポート8000が使用されていないか確認

### API呼び出しエラー
- .envファイルのAPIキーが正しいか確認
- APIキーの利用制限に達していないか確認

## サンプル調査トピック

- "2025年のAI技術トレンドと企業への影響"
- "リモートワークが企業文化に与える長期的影響"
- "サステナビリティとESG投資の最新動向"
- "デジタルトランスフォーメーションの成功要因分析"

## 次のステップ

- スライドテンプレートのカスタマイズ
- 追加のAIモデルの統合
- 調査結果のエクスポート機能の拡張