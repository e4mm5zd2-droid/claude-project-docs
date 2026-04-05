# Mac mini AIサーバー構成
*自動生成: 2026-04-04*

## マシンスペック
- チップ: Apple M4 (10コア: 4パフォーマンス + 6効率)
- メモリ: 24 GB
- OS: macOS 26.2 (Build 25C56)
- ストレージ: （標準SSD）
- モデル: Mac mini (2024)
- シリアル: TQVHF4P7M9

## 稼働中サービス一覧

| サービス名 | 起動方式 | リポジトリ | ポート | 状態 | 概要 |
|---|---|---|---|---|---|
| KURODO統括Bot | tmux (kurodo) + cron healthcheck | kurodo-bot | - | 稼働中 | Telegram経由の経営AI（Claude Code操作） |
| HISHO Bot | tmux + cron healthcheck | hisho-bot | - | 稼働中 | Telegram経由の秘書AI（Claude Code操作） |
| テラスHISHO Bot | tmux + cron healthcheck | terrace-hisho-bot | - | 稼働中 | テラス用秘書Telegram Bot |
| テラス統括Bot | launchd (KeepAlive) + cron | terrace-sokatsu-bot | - | 稼働中 | テラス用経営Telegram Bot |
| 経費Bot | launchd (KeepAlive) | claude-project-docs/expense-bot | - | 稼働中 | Telegram経費入力Bot (Python 3.9) |
| Reels Overlay Tool | tmux (streamlit) | reels-overlay-tool | 8502 | 稼働中 | 動画オーバーレイ加工Webアプリ |
| NEXUS Research Engine | 手動起動 | nexus-research-engine | - | 停止中 | AI投資リサーチシステム |
| dev session | launchd (RunAtLoad) | - | - | 稼働中 | 開発環境セットアップスクリプト |

## tmuxセッション詳細

| セッション名 | ウィンドウ数 | 実行中コマンド | 用途 |
|---|---|---|---|
| kurodo | 複数 | /opt/homebrew/bin/tmux | KURODO Bot + 各種Bot管理 |

## LaunchAgents一覧

| plistファイル名 | 実行対象 | 間隔 | 状態 |
|---|---|---|---|
| com.ontheedge.dev.plist | start_dev.sh | RunAtLoad | 稼働中 |
| com.ontheedge.terrace-sokatsu-bot.plist | terrace-sokatsu-bot/start.sh | KeepAlive + RunAtLoad | 稼働中 |
| com.ote.expense-bot.plist | expense-bot/main.py (Python) | KeepAlive + RunAtLoad | 稼働中 |

## リポジトリ一覧

| リポジトリ | パス | 概要 | 主要技術 | CLAUDE.md | README.md |
|---|---|---|---|---|---|
| claude-project-docs | ~/Projects/claude-project-docs | 全Project共通ドキュメントリポジトリ。Claude Projects GitHub連携用 | Python, Markdown | ✅ | ✅ |
| hisho-bot | ~/Projects/hisho-bot | HISHO Telegram Bot。Claude Code操作で秘書業務を実行 | Bash, Telegram Bot | ❌ | ❌ |
| hisho-workspace | ~/Projects/hisho-workspace | HISHO作業用ワークスペース。タスク管理・リサーチ・議事録 | Claude Code | ✅ | ❌ |
| keihi-workspace | ~/Projects/keihi-workspace | 経費管理ボット作業用ワークスペース | Claude Code | ✅ | ❌ |
| kurodo-bot | ~/Projects/kurodo-bot | KURODO Telegram Bot。Claude Code操作でclaude-project-docsを管理 | Bash, Telegram Bot | ❌ | ❌ |
| nexus-research-engine | ~/Projects/nexus-research-engine | AI投資リサーチシステム。5ソース横断検索+AIスコアリング | Python 3.11, Claude API, xAI Grok, Supabase, pgvector | ✅ | ✅ |
| reels-overlay-tool | ~/Projects/reels-overlay-tool | Reels/TikTok/Shorts動画オーバーレイ加工ツール | Python 3.11, Streamlit, FFmpeg, Pillow | ✅ | ✅ |
| terrace-hisho-bot | ~/Projects/terrace-hisho-bot | テラス用HISHO Telegram Bot | Bash, Telegram Bot | ❌ | ❌ |
| terrace-sokatsu-bot | ~/Projects/terrace-sokatsu-bot | テラス用統括Telegram Bot | Bash, Telegram Bot | ❌ | ❌ |

## ネットワーク・ポート使用状況

| ポート | プロセス | 用途 |
|---|---|---|
| 8502 | Python (Streamlit) | reels-overlay-tool Web UI |
| 7000 | ControlCenter | AirPlay |
| 5000 | ControlCenter | AirPlay |
| 49152 | rapportd | macOSシステムサービス |
| 8770 | sharingd | macOS共有サービス |

※ Telegram Botはすべてアウトバウンド（ロングポーリング）のため、LISTENポートなし

## cron / 定期実行タスク

| スケジュール | コマンド | 用途 |
|---|---|---|
| */15 * * * * | kurodo-bot/healthcheck.sh | KURODO Bot死活監視 |
| */15 * * * * | hisho-bot/healthcheck.sh | HISHO Bot死活監視 |
| */15 * * * * | terrace-sokatsu-bot/healthcheck.sh | テラス統括Bot死活監視 |
| */15 * * * * | terrace-hisho-bot/healthcheck.sh | テラスHISHO Bot死活監視 |
| */15 * * * * | healthcheck.sh | 全体ヘルスチェック |
| 0 9 1 * * | expense-bot/jobs/monthly_report_job.py | 月次経費レポート（毎月1日 9:00） |

## 環境変数（キー名のみ、値は含まない）

### hisho-bot / kurodo-bot / terrace-hisho-bot / terrace-sokatsu-bot（共通）
- TELEGRAM_BOT_TOKEN
- ALLOWED_USER_IDS
- REPO_DIR
- CLAUDE_PATH

### nexus-research-engine
- TELEGRAM_BOT_TOKEN
- TELEGRAM_ALLOWED_USERS
- ANTHROPIC_API_KEY
- XAI_API_KEY
- DATABASE_URL
- NRE_MAX_RESULTS_PER_SOURCE
- NRE_MIN_SCORE_THRESHOLD
- NRE_REPORT_DIR
- NRE_LOG_LEVEL
