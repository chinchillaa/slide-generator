# CLAUDE.md - プロジェクトガイドライン

## 1. スライド作成時の重要な参考資料

### デザインとカラーの参考
work/slide_generator/reference/sample.html を参照し、デザインやカラーを統一すること

- **メイン参照ファイル**: `sample.html` - 全6スライドの統合版
- このファイルには、スライドデザインの標準的なガイドラインが含まれています
- カラースキーム、フォント、レイアウトなどの統一性を保つため、必ず参照してください
- ブランドガイドラインに準拠したデザインを心がけてください
- ナビゲーション機能付きで、全スライドを簡単に確認できます
- **注意**: `reference/archive/` 以下のファイルは参照不要（旧バージョンのため）

### 企業ロゴの配置
**必須**: 全てのスライドに企業ロゴ「= SB C&S」を配置すること

- 位置: 右上（top: 20px, right: 20px）
- スタイル:
  ```html
  <div class="logo flex items-center">
      <span class="text-gray-400 mr-2">=</span>SB C&S
  </div>
  ```
- CSSクラス:
  ```css
  .logo {
      position: absolute;
      top: 20px;
      right: 20px;
      font-weight: bold;
      color: #888;
      font-size: 24px;
  }
  ```

## 2. スライドデザインの共通パターン（参考資料分析結果）

### 2.1 基本レイアウト構造
- **スライドサイズ**: 1280px × 720px（16:9比率）
- **背景色**: 白（#FFFFFF）
- **パディング**: 上下左右 40px（p-10）
- **ロゴ配置**: 右上（top: 20px, right: 20px）固定位置
- **フォントファミリー**: 'Hiragino Sans', 'Meiryo', sans-serif（日本語対応）

### 2.2 カラースキーム
#### メインカラー
- **紫色（パープル）**: #8a2be2（RGB: 138, 43, 226）
  - タイトルのアクセントライン
  - 数値のハイライト
  - アイコンの背景色（15%透明度: rgba(138, 43, 226, 0.15)）
  - ボーダー色

#### サポートカラー
- **緑色（グリーン）**: #22c55e（正の数値・改善・増加を表現）
- **赤色（レッド）**: #e53e3e（負の数値・減少・マイナスを表現）
- **グレー**: 
  - #666666（サブタイトル）
  - #888888（ロゴ）
  - #e2e8f0（ボーダー）
  - #f9fafb（背景のアクセント）

### 2.3 タイポグラフィ
- **メインタイトル**: text-5xl（初回）、text-3xl（各ページ）、font-bold
- **サブタイトル**: text-4xl、text-purple-800
- **セクションタイトル**: text-xl、font-bold
- **数値強調**: text-2.5rem～1.8rem、font-bold、color: #8a2be2
- **本文**: text-base（デフォルト）
- **注釈**: text-sm、text-gray-600

### 2.4 共通UIコンポーネント

#### タイトルボックス
```css
.title-box {
    border-left: 8px solid #8a2be2;
    padding-left: 20px;
    margin-bottom: 30px;
}
```

#### アイコンサークル
```css
.icon-circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: rgba(138, 43, 226, 0.15);
    display: flex;
    align-items: center;
    justify-content: center;
}
```

#### データアイテム
- 左側にアイコンサークル
- 右側にコンテンツ
- margin-bottom: 20-25px

#### セグメントボックス
- border: 1px solid #e2e8f0
- border-radius: 8px
- padding: 15px
- hover時: box-shadow追加

### 2.5 アイコン使用パターン（Font Awesome）
- **財務系**: fa-chart-line, fa-calculator, fa-money-bill-wave, fa-balance-scale
- **組織系**: fa-building, fa-building-columns
- **技術系**: fa-microchip, fa-robot, fa-cogs
- **モバイル系**: fa-mobile-alt
- **投資系**: fa-chart-pie, fa-coins
- **方向性**: fa-arrow-up（増加）, fa-arrow-down（減少）
- **その他**: fa-angle-right（リスト項目）, fa-info-circle（注釈）

### 2.6 レイアウトパターン
1. **タイトルページ**: 中央配置、紫のアクセントライン、グラデーション
2. **データ表示ページ**: 
   - 左側：メインデータ
   - 右側：詳細・補足情報（グレー背景）
3. **セグメント表示**: 2×2グリッド配置
4. **リスト表示**: アイコン + テキストの組み合わせ

### 2.7 視覚的階層
1. **レベル1**: メインタイトル（紫のボーダー付き）
2. **レベル2**: セクションタイトル（アイコン付き）
3. **レベル3**: データ項目（数値は紫で強調）
4. **レベル4**: 補足説明（グレーテキスト）

### 2.8 アニメーション・インタラクション
- ホバー効果: box-shadow追加、border-color変更
- transition: all 0.3s ease

### 2.9 注意事項
- 数値は必ず紫色（#8a2be2）で強調
- 増減は緑（増加）・赤（減少）で色分け
- 重要な情報は背景色（薄紫: bg-purple-50）で囲む
- ページ下部に必ず注釈エリアを設置（text-sm、text-gray-600）