# Hugging Face Token パーミッション設定ガイド

## 必要なパーミッション

Deep Research Slides Generatorで使用するHugging Face Token（HF_TOKEN）には、以下のパーミッションが必要です：

### 1. **Read access to contents of all public gated repos you can access**
- ✅ 必須
- 公開されているがゲート付きのリポジトリ（アクセス許可が必要なモデル）へのアクセスに必要
- 例：LLaMA、Falcon、その他の制限付きモデル

### 2. **Write access to your personal repos**
- ⚪ オプション（推奨）
- エージェントやツールをHugging Face Hubに保存する場合に必要
- 将来的にカスタムエージェントを共有する場合に便利

### 3. **Access to Inference API**
- ✅ 必須
- Hugging Face Inference APIを使用してモデルを実行する場合に必要
- `InferenceClientModel`を使用する場合は特に重要

## トークンの作成手順

1. [Hugging Face Settings](https://huggingface.co/settings/tokens)にアクセス
2. "New token"をクリック
3. トークン名を入力（例：`deep-research-slides`）
4. 以下の権限を選択：
   - ✅ Read access to contents of all public gated repos you can access
   - ✅ Access to Inference API
   - ⚪ Write access to your personal repos（オプション）
5. "Generate token"をクリック

## セキュリティのベストプラクティス

### 1. **最小権限の原則**
```bash
# 本番環境では読み取り専用トークンを使用
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx  # Read-only token
```

### 2. **トークンのローテーション**
- 定期的にトークンを更新（3-6ヶ月ごと）
- 古いトークンは無効化

### 3. **環境ごとの分離**
```bash
# 開発環境
HF_TOKEN_DEV=hf_dev_xxxxxxxxxxxxx

# 本番環境
HF_TOKEN_PROD=hf_prod_xxxxxxxxxxxxx
```

### 4. **トークンの保護**
```bash
# .envファイルをGitに含めない
echo ".env" >> .gitignore

# 環境変数として設定
export HF_TOKEN="your_token_here"
```

## トークンが必要な機能

### 1. **モデルアクセス**
- ゲート付きモデル（LLaMA、Falcon等）の使用
- プライベートモデルへのアクセス

### 2. **Inference API**
```python
from smolagents import InferenceClientModel

# HF_TOKENが必要
model = InferenceClientModel(
    model_id="meta-llama/Llama-2-7b-hf",
    token=os.getenv("HF_TOKEN")
)
```

### 3. **Hub統合**
```python
from smolagents import Tool

# ツールの共有（Write権限が必要）
tool.push_to_hub("username/tool-name")

# ツールの取得（Read権限が必要）
tool = Tool.from_hub("username/tool-name")
```

## トラブルシューティング

### エラー: "401 Unauthorized"
```bash
# トークンが正しく設定されているか確認
echo $HF_TOKEN

# トークンの権限を確認
# Hugging Face Settingsでトークンの権限を再確認
```

### エラー: "403 Forbidden"
```bash
# ゲート付きモデルへのアクセス許可が必要
# 1. モデルページで利用規約に同意
# 2. アクセスが承認されるまで待つ
```

### エラー: "Model not found"
```python
# プライベートモデルの場合、明示的にトークンを渡す
model = InferenceClientModel(
    model_id="username/private-model",
    token=os.getenv("HF_TOKEN"),
    private=True
)
```

## 推奨設定

開発環境では以下の設定を推奨：

```bash
# .env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxx  # Read + Inference API access
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
SERPER_API_KEY=xxxxxxxxxxxxx
```

## セキュリティチェックリスト

- [ ] トークンに最小限の権限のみ付与
- [ ] .envファイルが.gitignoreに含まれている
- [ ] 本番環境では環境変数を使用
- [ ] トークンを定期的にローテーション
- [ ] アクセスログを定期的に確認

## 参考リンク

- [Hugging Face Token管理](https://huggingface.co/docs/hub/security-tokens)
- [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index)
- [smolagents ドキュメント](https://huggingface.co/docs/smolagents)