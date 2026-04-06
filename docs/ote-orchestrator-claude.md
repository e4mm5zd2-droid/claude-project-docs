# ote-orchestrator

## 概要
株式会社on the edgeの全AIシステムを統合するオーケストレーション層。
「情報収集→AI分析→推奨アクション→承認→タスク化」の自動ループを実現する。

## コードスタイル
- Python 3.9+（Mac mini互換）
- from __future__ import annotations 必須
- 各モジュールのdocstringにInputs/Outputsを明記
- 外部API呼び出しは必ずtry-exceptでラップ
- 1ステップの失敗が全体を止めない設計（各ステップ独立実行）

## アーキテクチャ
- collectors/ : 4ソースからデータ収集（ai-intel, expense, tasks, KPI）
- analyzers/  : Claude APIで統合分析
- dispatchers/: Telegram（アクション）+ Discord（アーカイブ）に配信
- handlers/   : 承認/却下の受信→MASTER_TASKS更新→git push
- jobs/       : cronジョブ（daily_briefing, weekly_report）

## 環境変数（キー名のみ）
- ANTHROPIC_API_KEY
- TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID_TAKA / TELEGRAM_CHAT_ID_MATSUMOTO / TELEGRAM_CHAT_ID_TERRACE
- DISCORD_GENERAL_WEBHOOK_URL / DISCORD_INTEL_WEBHOOK_URL
- GOOGLE_SERVICE_ACCOUNT_JSON_PATH / EXPENSE_SHEETS_ID
- SUPABASE_URL / SUPABASE_KEY
- CLAUDE_PROJECT_DOCS_PATH / MASTER_TASKS_PATH

## テスト実行
```bash
# デイリーブリーフィングの手動テスト
cd ~/Projects/ote-orchestrator
source venv/bin/activate
python -m jobs.daily_briefing
```

## cron設定
```bash
# 毎朝9:00 JST
0 9 * * * cd /Users/on-the-edge/Projects/ote-orchestrator && /Users/on-the-edge/Projects/ote-orchestrator/venv/bin/python -m jobs.daily_briefing >> /Users/on-the-edge/Projects/ote-orchestrator/logs/daily_briefing.log 2>&1
```

## 禁止事項
- .envファイルをgitにコミットしない
- APIキーやトークンをログに出力しない
- service_account.jsonをgitにコミットしない

## 依存システム
- ai-intel-pipeline（Render）→ Supabase経由でデータ取得
- expense-bot（Mac mini）→ Google Sheets経由でデータ取得
- claude-project-docs（Mac mini）→ MASTER_TASKS.mdをローカル参照
- KURODO Telegram Bot（Mac mini）→ Bot Tokenを共有して送信
