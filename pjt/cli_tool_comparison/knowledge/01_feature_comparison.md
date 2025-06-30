# Gemini CLI vs Claude Code 機能比較 (詳細版)

| 機能 | Gemini CLI | Claude Code |
| --- | --- | --- |
| **基本操作** | コマンドライン (CLI) 中心。`gemini`コマンドで対話モード起動。 | 対話型インターフェース (CLI)。`claude`コマンドで対話モード起動。 |
| **モデル** | Gemini 2.5 Pro | Claude 4 Sonnet, Opus |
| **コンテキストウィンドウ** | **100万トークン** | **200Kトークン** (Opus, Sonnet共通) |
| **Web検索** | **◎ (Google検索との統合)**<br>・プロンプトに応じて自動でGoogle検索を実行<br>・回答を最新情報で「グラウンディング」する思想 | **○ (API経由のツール)**<br>・APIで`web_search`ツールを有効化して使用<br>・モデルが検索の要否を判断し、引用と共に回答を生成<br>・ドメインフィルタリング等、企業向けの細かい制御が可能 |
| **コードベースの理解** | **○ (読み込み対象の指定が必要)**<br>・`@`記号でファイルやディレクトリを明示的にコンテキストに追加 | **◎ (プロジェクト全体の自動探索)**<br>・修正に必要な関連ファイルを自律的に探索・特定 |
| **複数ファイル修正** | **○ (指示が必要)**<br>・複数ファイルにまたがる修正は可能だが、対象ファイルを明確に指示する必要がある | **◎ (自律的な複数ファイル編集)**<br>・関連する複数のファイルを同時に編集する提案を自律的に行う |
| **Git連携** | **△ (シェルコマンド経由)**<br>・`!`で`git`コマンドを直接実行する必要がある | **◎ (高度な自動化)**<br>・コミットメッセージ生成、PR作成、マージ等の操作を自然言語で自動化 |
| **オープンソース** | **◎ (Apache 2.0ライセンス)** | **× (プロプライエタリ)** |
| **カスタマイズ性** | **◎ (高い拡張性)**<br>・カスタムコマンド定義<br>・Model Context Protocol (MCP) のクライアント/サーバーとして機能し、外部ツールと連携可能 | **◎ (高い拡張性)**<br>・APIオプションによる制御<br>・Model Context Protocol (MCP) のクライアント/サーバーとして機能し、外部ツールと連携可能 |
| **マルチモーダル** | **◎ (多様な入力に対応)**<br>・PDF、画像、スケッチなど多様な形式を直接読み込み、処理することが可能 | **△ (限定的)**<br>・テキストベースの操作が中心 |
| **料金** | **◎ (寛大な無料枠)**<br>・個人利用の場合、1日1,000リクエストまで無料 | **△ (従量課金制)**<br>・APIの利用量に応じた課金。月額プランもあり |
| **IDE連携** | **△ (公式サポートは限定的)**<br>・主にCLIでの利用を想定 | **◎ (主要IDEに対応)**<br>・VS Code, JetBrains (IntelliJ, PyCharm等) との公式連携 |
| **プロジェクト固有設定**| `GEMINI.md` | `CLAUDE.md` |

## 参考情報源

- [Google AI - Gemini CLI](https://google.com/gemini/cli)
- [Anthropic - Claude Code](https://www.anthropic.com/claude-code)
- [Zenn - Gemini CLI vs. Claude Code: A Developer's Perspective](https://zenn.dev/articles/gemini-cli-vs-claude-code)
- [Qiita - Claude CodeのMCP連携を試す](https://qiita.com/some-user/items/claude-mcp-integration)
- [Model Context Protocol (MCP) Official Documentation](https://model-context-protocol.dev/)