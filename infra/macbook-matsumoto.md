# MacBook Air 開発環境構成
*自動生成: 2026-04-06*

## マシンスペック
- チップ: Apple M3（8コア: 4パフォーマンス + 4エフィシェンシー）
- メモリ: 24 GB
- OS: macOS 26.3.1 (Build 25D2128)
- ストレージ: 460GB（使用 12GB / 空き 308GB）
- モデル: MacBook Air (Mac15,12) MC8N4J/A

## 開発リポジトリ一覧

| リポジトリ | パス | 概要 | Mac miniにもあるか | 主要技術 |
|---|---|---|---|---|
| archive | ~/Projects/archive | レガシー保管庫（Knowledge_Base、旧SaaS等） | × | — |
| business1-crypto-affiliate | ~/Projects/business1-crypto-affiliate | 事業1関連（プレースホルダー） | × | — |
| business2-x-tools | ~/Projects/business2-x-tools | ai-intel-pipeline、x-auto-bot、x-video-botのコンテナ | × | Python |
| business3-kyoto-nightwork | ~/Projects/business3-kyoto-nightwork | SmartNRナイトワークスカウトアプリ＆ツール | × | FastAPI/Python |
| claude-project-docs | ~/Projects/claude-project-docs | Claude Projects自動同期用ドキュメント集約 | ○ | Python/Markdown |
| crypto-everyday-bridge | ~/Projects/crypto-everyday-bridge | クリプト/DeFiディスカバリーWebアプリ | × | React/Vite/Node.js |
| docs | ~/Projects/docs | NEXUS株式スカウティング仕様書 | × | Markdown |
| fonts | ~/Projects/fonts | UI描画用フォントライブラリ（ipaexg.ttf） | × | — |
| kurodo-pet | ~/Projects/kurodo-pet | ロックマンエグゼ風AIエージェント操作ダッシュボード | ○ | Next.js 16/TypeScript/Tailwind |
| nexus-research-engine | ~/Projects/nexus-research-engine | 5ソース横断検索+AIスコアリングTelegramボット | ○ | Python/PostgreSQL/pgvector |
| on-the-edge-corporate-v2 | ~/Projects/on-the-edge-corporate-v2 | on the edge コーポレートサイト | × | React/Vite/Node.js |
| prediction-engine | ~/Projects/prediction-engine | NEXUS 5セクター株式スクリーナー | × | Python/Streamlit/XGBoost |
| rabbit-photos | ~/Projects/rabbit-photos | うさぎ写真分析用iCloud共有フォルダ参照 | × | iCloud/Markdown |
| rabbit-video-project | ~/Projects/rabbit-video-project | ワンコマンド動画処理パイプライン | × | Python/Make/FFmpeg |
| shared | ~/Projects/shared | 共有ユーティリティ（docs, skills, logs等） | × | Python |
| tools | ~/Projects/tools | ユーティリティスクリプト（Render env copy等） | × | Python/Shell |
| toto-prediction-system | ~/Projects/toto-prediction-system | toto/WINNER AI予測システム | × | Python 3.11/XGBoost/Streamlit/SQLite |
| x-auto-bot | ~/Projects/x-auto-bot | crypto_0101010ボット（12アカウント監視+リツイート+AI書換） | × | Python/Node.js |
| yt-x-thread-bot | ~/Projects/yt-x-thread-bot | YouTube→X自動スレッド投稿ボット | × | Python/PostgreSQL |

## 開発ツール

| ツール | バージョン | パス | 用途 |
|---|---|---|---|
| Cursor | — | /usr/local/bin/cursor | AI開発IDE |
| Claude Code | 2.1.90 (Native) | ~/.local/bin/claude | CLI AI開発ツール |
| Node.js | v20.20.0 | nvm管理 | JS実行環境 |
| Python | 3.14.3 | Homebrew | Python実行環境 |
| npm | nvm管理 | nvm管理 | パッケージ管理 |
| Deno | Homebrew | Homebrew | JSランタイム |
| FFmpeg | Homebrew | Homebrew | 動画・音声処理 |
| gh (GitHub CLI) | Homebrew | Homebrew | GitHub操作 |
| Git | Homebrew | Homebrew | バージョン管理 |

## SSH接続先
- SSH configファイルなし（Tailscale VPN経由で直接IP接続）
- Mac mini: `ssh on-the-edge@100.111.159.72`

## Git設定
- user.name: kyo
- user.email: keyvon.722.btf@gmail.com

## 開発ワークフロー
- Cursor: Claude Opus 4.6 使用、`/effort ultrathink` 適用
- Claude Code: `~/.local/bin/claude` (Native版 v2.1.90)
- デプロイ: MacBook (開発) → `git push` → Mac mini (`git pull` → 再起動)
- Mac miniへのSSH: Tailscale VPN経由（100.111.159.72）
