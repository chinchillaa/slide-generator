# Slide Generator

プロフェッショナルなスライドを生成するツール - SB C&Sブランディング準拠

## 概要

このプロジェクトは、統一されたデザインとブランディングに基づいて、プロフェッショナルなプレゼンテーションスライドを生成するツールです。

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

## 使用方法

### 参考スライドの確認
```bash
# ブラウザで開く
open reference/sample.html
```

### 新しいスライドの作成
1. `reference/sample.html`のデザインを参考にする
2. CLAUDE.mdのガイドラインに従う
3. 必要なセクションをコピー・編集

## サンプルプロジェクト

### UiPath Insights
- 場所: `pjt/UiPath/`
- 内容: UiPath Insightsの特徴と活用事例

### クラウドサービス比較
- 場所: `pjt/major_cloud_service/`
- 内容: AWS、Azure、GCPの比較分析

## ライセンス

このプロジェクトは内部使用を目的としています。

---

🤖 Generated with [Claude Code](https://claude.ai/code)