# Slide Generator

社内向けClaude Code活用プロジェクト - 調査・資料作成の工数削減ツール

## 🎯 プロジェクトの目的

このリポジトリは、**社内でClaude Codeを活用して調査・資料作成の工数を大幅に削減する**ことを目的としています。

### 主な利用シーン
- 📊 **調査レポートの自動生成**: 市場調査、競合分析、技術調査など
- 📝 **プレゼン資料の効率的作成**: 統一されたデザインでの資料作成
- ⏱️ **作業時間の短縮**: 従来の手作業から自動生成への移行
- 🔄 **品質の標準化**: ブランドガイドラインに準拠した一貫性のある成果物

## 概要

このプロジェクトは、Claude Codeと連携して動作し、統一されたデザインとブランディングに基づいて、プロフェッショナルなプレゼンテーションスライドを自動生成するツールです。

## 特徴

- 🎨 **統一されたデザイン**: SB C&Sブランディングガイドラインに準拠
- 🎯 **紫色のアクセントカラー**: #8a2be2をメインカラーとして使用
- 📊 **データビジュアライゼーション**: 財務データや統計情報の見やすい表示
- 🔄 **HTML to PPTX変換**: HTMLスライドをPowerPoint形式に変換可能
- 📱 **レスポンシブデザイン**: 様々な画面サイズに対応

## ディレクトリ構造

```
slide-generator/
├── reference/          # 参考スライドテンプレート
│   └── sample.html    # 統合版サンプルスライド（全6ページ）
├── pjt/               # プロジェクトサンプル
│   ├── UiPath/        # UiPath Insightsスライド
│   └── major_cloud_service/  # クラウドサービス比較スライド
├── html_to_pptx/      # HTML to PPTX変換ツール
└── CLAUDE.md          # デザインガイドライン
```

## デザインガイドライン

### カラースキーム
- **メインカラー（紫）**: #8a2be2
- **ポジティブ（緑）**: #22c55e
- **ネガティブ（赤）**: #e53e3e
- **グレー系**: #666666, #888888, #e2e8f0

### レイアウト
- スライドサイズ: 1280px × 720px（16:9）
- パディング: 40px
- 企業ロゴ: 右上固定（"= SB C&S"）

## Claude Codeでの使用方法

### 1. 調査・分析の依頼
```
Claude Codeに調査したいテーマを伝えます：
例: "UiPath Insightsについて調査し、スライドを作成してください"
```

### 2. 自動生成プロセス
Claude Codeが以下を自動実行：
1. テーマに関する情報収集・分析
2. `reference/sample.html`のデザインに基づくスライド生成
3. CLAUDE.mdのガイドラインに準拠した成果物作成

### 3. カスタマイズ
生成されたスライドは必要に応じて編集可能：
- HTMLファイルを直接編集
- デザインテンプレートの調整
- コンテンツの追加・修正

## サンプルプロジェクト（Claude Code生成例）

### UiPath Insights 調査資料
- 場所: `pjt/UiPath/`
- 生成時間: 約5分
- 内容: UiPath Insightsの特徴、メリット、活用事例の包括的な調査結果

### クラウドサービス比較分析
- 場所: `pjt/major_cloud_service/`
- 生成時間: 約10分
- 内容: AWS、Azure、GCPの詳細な比較分析と推奨事項

## 🚀 導入効果

### 工数削減の実績
- **調査時間**: 2-3日 → 10-30分
- **資料作成**: 1-2日 → 5-15分
- **品質**: 属人性を排除し、一定品質を保証

### ROI（投資対効果）
- 調査・資料作成業務の80%以上の工数削減
- 社員がより創造的な業務に集中可能
- ミスや抜け漏れの削減

## 📌 注意事項

- このツールは社内利用専用です
- Claude Codeとの連携が必要です
- 生成された内容は必ず人間がレビューしてください

---

🤖 Generated with [Claude Code](https://claude.ai/code)