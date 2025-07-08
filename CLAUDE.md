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

### 4.1 よくある問題と対策

#### 囲み枠のはみ出し問題
**問題**: segment-boxやコンテンツボックスが親要素からはみ出す
**原因**: 
- 固定幅の設定
- パディングとマージンの累積
- グリッドのギャップが大きすぎる

**対策**:
```css
.segment-box {
    /* height: 100%; を削除 */
    max-width: 100%;
    overflow: hidden;
}
```

#### グリッドレイアウトの調整
**問題**: 2カラムレイアウトで右側のコンテンツがはみ出す
**対策**:
- `gap-x-10` → `gap-x-8` または `gap-6` に変更
- 親要素に `max-width: 100%` を追加
- 内部要素のフォントサイズを調整

#### 固定高さスライドでの下部切れ問題
**問題**: 720pxの固定高さで下部のコンテンツが見切れる
**対策**:
```css
/* 注釈の位置を絶対配置に */
position: absolute;
bottom: 80px;
left: 40px;
```
- マージンとパディングを削減（mt-8 → mt-6、mb-4 → mb-3）
- コンテンツの分量を調整

### 4.2 レイアウトチェックリスト
1. **全体の制約**
   - スライドサイズ: 1280px × 720px（変更不可）
   - overflow: hidden（必須）
   
2. **コンテンツの配置**
   - 左右マージン: 40px
   - 上部: ロゴエリア確保（60px）
   - 下部: ナビゲーション確保（80px）
   
3. **グリッドシステム**
   - 2カラム: gap-6 または gap-8
   - 3カラム以上: gap-3 または gap-4
   
4. **フォントサイズの調整**
   - スペースが限られる場合は段階的に縮小
   - 最小サイズ: text-xs（12px）

### 4.3 デバッグ方法
1. ブラウザの開発者ツールで要素のサイズを確認
2. 親要素の幅を超えていないかチェック
3. box-sizingがborder-boxになっているか確認
4. 累積マージン・パディングを計算

### 4.4 グレー背景要素内での注意事項
**問題**: bg-gray-50などの背景要素内で、子要素（特にbg-green-100などの強調ボックス）がはみ出す
**対策**:
1. 親要素に必ず以下を追加:
   ```html
   style="max-width: 100%; overflow: hidden;"
   ```
2. 子要素のマージンを調整:
   - 最下部の要素には `style="margin: 0;"` を追加
   - feature-boxなどには明示的に `mb-3` を追加して間隔を統一
3. フォントサイズの調整:
   - はみ出しそうな場合は `text-2xl` → `text-xl` に縮小
   - 情報量が多い場合は階層化して整理