# CLAUDE.md - プロジェクトガイドライン

## 1. スライドの保存場所

### 重要：スライド作成時のディレクトリ構造
**全てのスライドは `work/slide_generator/pjt/[プロジェクト名]/slides/` 以下に作成すること**

- スライドファイルの保存先: `pjt/[プロジェクト名]/slides/`
- 例：
  - `pjt/major_cloud_service/slides/`
  - `pjt/snowflake_research/slides/`
  - `pjt/cli_tool_comparison/slides/`
  - `pjt/softbank_ai_agents/slides/`
  - `pjt/UiPath/slides/`
  - `pjt/gemini_claude_comparison/slides/`

### ファイル命名規則
- HTMLファイル: `slide_01.html`, `slide_02.html`, ... （連番）
- または内容を表すファイル名: `title.html`, `overview.html`, `comparison.html` など

## 2. スライド作成時の重要な参考資料

### デザインとカラーの参考
work/slide_generator/reference/sample_green.html を参照し、デザインやカラーを統一すること

- **メイン参照ファイル**: `sample_green.html` - 全6スライドの統合版（緑色基調）
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

## 3. スライドデザインの共通パターン（参考資料分析結果）

### 3.1 基本レイアウト構造
- **スライドサイズ**: 1280px × 720px（16:9比率）
- **背景色**: 白（#FFFFFF）
- **パディング**: 上下左右 40px（p-10）
- **ロゴ配置**: 右上（top: 20px, right: 20px）固定位置
- **フォントファミリー**: 'Hiragino Sans', 'Meiryo', sans-serif（日本語対応）

### 3.2 カラースキーム
#### メインカラー
- **緑色（グリーン）**: #22c55e（RGB: 34, 197, 94）
  - タイトルのアクセントライン
  - 数値のハイライト
  - アイコンの背景色（15%透明度: rgba(34, 197, 94, 0.15)）
  - ボーダー色

#### サポートカラー
- **緑色（グリーン）**: #22c55e（正の数値・改善・増加を表現）
- **赤色（レッド）**: #e53e3e（負の数値・減少・マイナスを表現）
- **グレー**: 
  - #666666（サブタイトル）
  - #888888（ロゴ）
  - #e2e8f0（ボーダー）
  - #f3f4f6（背景）
  - #f9fafb（背景のアクセント）

### 3.3 タイポグラフィ
- **メインタイトル**: text-5xl（初回）、text-3xl（各ページ）、font-bold
- **サブタイトル**: text-4xl、text-green-800
- **セクションタイトル**: text-xl、font-bold
- **数値強調**: text-2.5rem～1.8rem、font-bold、color: #22c55e
- **本文**: text-base（デフォルト）
- **注釈**: text-sm、text-gray-600

### 3.4 共通UIコンポーネント

#### タイトルボックス
```css
.title-box {
    border-left: 8px solid #22c55e;
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
    background-color: rgba(34, 197, 94, 0.15);
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

### 3.5 アイコン使用パターン（Font Awesome）
- **財務系**: fa-chart-line, fa-calculator, fa-money-bill-wave, fa-balance-scale
- **組織系**: fa-building, fa-building-columns
- **技術系**: fa-microchip, fa-robot, fa-cogs
- **モバイル系**: fa-mobile-alt
- **投資系**: fa-chart-pie, fa-coins
- **方向性**: fa-arrow-up（増加）, fa-arrow-down（減少）
- **その他**: fa-angle-right（リスト項目）, fa-info-circle（注釈）

### 3.6 レイアウトパターン
1. **タイトルページ**: 中央配置、緑のアクセントライン、グラデーション
2. **データ表示ページ**: 
   - 左側：メインデータ
   - 右側：詳細・補足情報（グレー背景）
3. **セグメント表示**: 2×2グリッド配置
4. **リスト表示**: アイコン + テキストの組み合わせ

### 3.7 視覚的階層
1. **レベル1**: メインタイトル（緑のボーダー付き）
2. **レベル2**: セクションタイトル（アイコン付き）
3. **レベル3**: データ項目（数値は緑で強調）
4. **レベル4**: 補足説明（グレーテキスト）

### 3.8 アニメーション・インタラクション
- ホバー効果: box-shadow追加、border-color変更
- transition: all 0.3s ease

### 3.9 注意事項
- 数値は必ず緑色（#22c55e）で強調
- 増減は緑（増加）・赤（減少）で色分け
- 重要な情報は背景色（薄緑: bg-green-50）で囲む
- ページ下部に必ず注釈エリアを設置（text-sm、text-gray-600）

## 4. レイアウト問題の対策

### 4.1 スライドコンテナの基本制約

#### 固定サイズの制約を理解する
- **スライドコンテナ**: 1280px × 720px（変更不可）
- **実質利用可能領域**:
  - 幅: 1280px - 80px（左右margin各40px）= 1200px
  - 高さ: 720px - 140px（上部60px + 下部80px）= **580px**
  - ⚠️ **重要**: コンテンツの高さ合計は580pxを超えてはいけない

#### レイアウト制約の図解
```
┌─────────────────────────────────┐
│  ロゴエリア（60px）               │ ← 企業ロゴ固定位置
├─────────────────────────────────┤
│                                 │
│  コンテンツエリア（580px）         │ ← 実質的な作業領域
│                                 │
├─────────────────────────────────┤
│  ナビゲーション（80px）           │ ← 固定ナビゲーション
└─────────────────────────────────┘
```

### 4.2 よくある問題と根本的な対策

#### 問題1: グリッドレイアウトでのはみ出し
**原因**: ギャップが大きすぎてコンテンツが圧迫される
**推奨値**:
```css
/* ❌ 避けるべき設定 */
grid-cols-2 gap-10  /* 40pxは大きすぎる */
grid-cols-2 gap-x-10 gap-y-8  /* 縦横のギャップが大きい */

/* ✅ 推奨設定 */
grid-cols-2 gap-6  /* 24px：標準的な2カラム */
grid-cols-2 gap-4  /* 16px：コンテンツが多い場合 */
grid-cols-3 gap-3  /* 12px：3カラム以上 */
```

#### 問題2: マージン・パディングの累積
**原因**: 複数要素のmargin/paddingが累積して高さ超過
**推奨値**:
```css
/* タイトル部分 */
mt-6 (24px) → mt-4 (16px)  /* スライド2以降のタイトル */
mb-6 (24px) → mb-4 (16px)  /* セクション間の間隔 */

/* 通常要素 */
mb-4 (16px) → mb-3 (12px)  /* 標準的な要素間隔 */
mb-3 (12px) → mb-2 (8px)   /* 密集レイアウト時 */

/* 最下部要素 */
style="margin-bottom: 0;"  /* 必須：親要素からのはみ出し防止 */
```

#### 問題3: グレー背景（bg-gray-50）内でのはみ出し
**根本原因**: 親要素にoverflow制御がない
**必須の対策**:
```html
<!-- ❌ 問題のあるコード -->
<div class="bg-gray-50 p-4 rounded-lg">
  <div class="feature-box">...</div>
</div>

<!-- ✅ 正しいコード -->
<div class="bg-gray-50 p-4 rounded-lg" style="max-width: 100%; overflow: hidden;">
  <div class="feature-box mb-3">...</div>
  <div class="feature-box" style="margin-bottom: 0;">...</div> <!-- 最後の要素 -->
</div>
```

### 4.3 高さ管理のベストプラクティス

#### 1. スライド2以降の基本構造
```html
<!-- タイトル：40px -->
<div class="title-box mt-6" style="margin-left: 40px;">
  <h1 class="text-3xl font-bold">タイトル</h1>
</div>

<!-- メインコンテンツ：最大500px -->
<div class="mt-4" style="margin-left: 40px; margin-right: 40px;">
  <!-- ここに配置できる高さは約500px -->
</div>

<!-- 注釈（必要な場合）：絶対配置 -->
<div class="text-sm text-gray-600" style="position: absolute; bottom: 80px; left: 40px;">
  <p>※注釈テキスト</p>
</div>
```

#### 2. グリッドレイアウトの高さ計算例
```
2カラムレイアウトの場合：
- タイトル: 40px
- マージントップ: 16px (mt-4)
- コンテンツ高さ: 500px
- 合計: 556px < 580px ✅

3つのsegment-boxを縦に並べる場合：
- 各ボックス: 150px × 3 = 450px
- 間隔: 12px × 2 = 24px
- 合計: 474px < 500px ✅
```

### 4.4 フォントサイズの段階的調整

#### 情報量に応じた調整ガイド
```
標準的な情報量：
- タイトル: text-3xl
- セクション見出し: text-xl
- 本文: text-base

情報量が多い場合：
- タイトル: text-2xl（縮小）
- セクション見出し: text-lg（縮小）
- 本文: text-sm（縮小）

限界値：
- 最小フォントサイズ: text-xs（12px）
- これ以下は可読性の問題
```

### 4.5 デバッグチェックリスト

#### スライド作成時の確認項目
- [ ] コンテンツの総高さは580px以内か？
- [ ] グリッドのギャップは適切か？（2カラム：gap-6以下）
- [ ] グレー背景要素に`overflow: hidden`を設定したか？
- [ ] 最下部の要素に`margin-bottom: 0`を設定したか？
- [ ] 注釈は絶対配置にしたか？
- [ ] ブラウザの開発者ツールで実際の高さを確認したか？

#### 緊急時の対処法
1. **フォントサイズを1段階縮小**
   - text-3xl → text-2xl → text-xl
2. **マージンを1段階縮小**
   - mb-4 → mb-3 → mb-2
3. **グリッドギャップを縮小**
   - gap-6 → gap-4 → gap-3
4. **情報の優先順位を見直し**
   - 重要度の低い情報を削除または注釈へ移動

### 4.6 segment-boxの適切な使用

#### 高さ制御のルール
```css
.segment-box {
    /* ❌ height: 100%; は使用しない */
    /* ✅ 内容に応じた自然な高さ */
    max-width: 100%;
    overflow: hidden;
    padding: 15px;  /* 固定値 */
}
```

#### 複数segment-boxの配置
```html
<!-- 垂直配置の場合 -->
<div class="space-y-3">  <!-- 12pxの統一間隔 -->
  <div class="segment-box">...</div>
  <div class="segment-box">...</div>
  <div class="segment-box">...</div>
</div>

<!-- グリッド配置の場合 -->
<div class="grid grid-cols-2 gap-4">  <!-- 16pxの統一ギャップ -->
  <div class="segment-box">...</div>
  <div class="segment-box">...</div>
</div>
```