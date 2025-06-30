# Figmaでスライドを作成する方法

このドキュメントでは、HTMLスライドをFigmaで再現する方法を説明します。

## 方法1: Figma Pluginを使用した自動インポート

### 推奨プラグイン
1. **HTML to Figma** - HTMLコードを直接Figmaにインポート
2. **JSON to Figma** - JSONデータからFigmaデザインを生成
3. **Figma Tokens** - デザインシステムの値を管理

### 手順
1. Figmaでプラグインをインストール
2. `figma_slide_structure.json`のデータを使用
3. プラグインでインポート実行

## 方法2: Figma APIを使用したプログラマティックな作成

### 必要なもの
- Figma Personal Access Token
- Node.js環境

### サンプルコード

```javascript
// Figma APIを使用してフレームを作成
const figmaToken = 'YOUR_FIGMA_TOKEN';
const fileKey = '3CC3JpWL9dLlM4YcJZgR4Q';

async function createSlide(slideData) {
  const response = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes`, {
    method: 'POST',
    headers: {
      'X-Figma-Token': figmaToken,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      nodes: [{
        type: 'FRAME',
        name: slideData.title,
        x: 0,
        y: slideData.slide * 800,
        width: slideData.layout.width,
        height: slideData.layout.height,
        fills: [{
          type: 'SOLID',
          color: {
            r: 1,
            g: 1,
            b: 1,
            a: 1
          }
        }]
      }]
    })
  });
  
  return response.json();
}
```

## 方法3: 手動でのデザイン作成（推奨）

Figmaで直接デザインを作成する場合の手順：

### 1. スライドフレームの作成
- サイズ: 1280 x 720px
- 背景色: #FFFFFF
- 間隔: 各スライド間に100pxの余白

### 2. デザインシステムの設定

#### カラーパレット
```
Primary: #8A2BE2 (BlueViolet)
Secondary: #D8BFD8 (Thistle)
Background: #FFFFFF
Text Primary: #1A1A1A
Text Secondary: #666666
Success: #22C55E
Error: #E53E3E
Info: #3B82F6
```

#### タイポグラフィ
```
H1: 48px, Bold
H2: 36px, Bold
H3: 24px, Bold
Body: 16px, Regular
Small: 14px, Regular
```

### 3. コンポーネントの作成

#### アイコン付きセクション
- アイコンサークル: 40x40px, 背景色 rgba(138, 43, 226, 0.15)
- タイトル: H3サイズ, Primary色
- 本文: Bodyサイズ, Text Primary色

#### 価格バッジ
- 無料バッジ: 背景 #22C55E, 白文字, padding 4px 12px, 角丸 20px
- 有料バッジ: 背景 #E53E3E, 白文字, padding 4px 12px, 角丸 20px

#### テーブル
- ヘッダー背景: #8A2BE2, 白文字
- セル: padding 12px, ボーダー #E2E8F0

### 4. 各スライドの構成

#### スライド1: タイトル
- 紫のアクセントバー（高さ4px）
- メインタイトル（60px）
- サブタイトル（48px、紫色）
- 説明文とロゴ配置

#### スライド2: エグゼクティブサマリー
- 3つのセクション（価格、技術、エンタープライズ）
- 各セクションにアイコンと箇条書き
- 市場への影響ボックス

#### スライド3: 基本仕様比較
- 8行×3列のテーブル
- 強みセクション（2カラム）

#### スライド4: 価格分析
- 左側：価格モデル比較
- 右側：年間コスト比較チャート
- ROI分析ボックス

#### スライド5: 機能比較
- 4つのカテゴリ（2×2グリッド）
- 各カテゴリにGeminiとClaudeの機能リスト

#### スライド6: ユースケース別推奨
- 4つのユーザータイプ（2×2グリッド）
- 意思決定フローチャート

#### スライド7: 市場への影響
- 市場変革（3項目）
- 技術トレンド（短期・中期）
- 市場規模グラフ

#### スライド8: まとめ
- 主要な結論
- 最終推奨事項（3カラム）
- 行動指針
- クロージングメッセージ

## Figmaでの効率的な作業のヒント

1. **Auto Layout**を使用してレスポンシブなレイアウトを作成
2. **Components**で再利用可能な要素を作成
3. **Styles**でカラーとテキストスタイルを統一
4. **Variants**でコンポーネントの状態を管理
5. **Plugins**で作業を自動化

## エクスポート

作成後のエクスポート形式：
- プレゼンテーション用: PDF
- Web用: PNG/SVG
- 開発用: CSS/JSON

---

このガイドを参考に、Figmaでプロフェッショナルなスライドを作成してください。