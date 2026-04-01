# expense-bot - OTE経費管理ボット

## コードスタイル
- Python 3.11+、python-telegram-bot v21
- Claude Vision API呼び出しは必ずtry-exceptでラップ
- Google Sheets APIのクォータ制限に注意（100 req/100sec）
- Claude モデル: claude-sonnet-4-20250514

## ワークフロー
- Mac mini常時稼働（launchd: com.ote.expense-bot.plist、Polling方式）
- テスト時はTelegram Bot Tokenをテスト用に切り替え
- `git push` は手動で行う（自動pushしない）

## アーキテクチャ
- main.py: エントリポイント（Telegram Polling）
- handlers/: Telegramコマンドハンドラ
- services/: Claude Vision OCR、Google Sheets書き込み
- models/: データモデル
- フロー: レシート画像受信 → Claude Vision OCR → 勘定科目分類 → Google Sheets書き込み

## 環境変数
- TELEGRAM_BOT_TOKEN, ALLOWED_USER_IDS
- ANTHROPIC_API_KEY
- GOOGLE_SHEETS_ID, GOOGLE_SERVICE_ACCOUNT_JSON

## 事業マスター
全社(0), アフィリ(1), Xツール(2), 求人(3), CRM(4)

## 禁止事項
- IMPORTANT: service_account.jsonをgitにコミットしない
- IMPORTANT: Telegram Bot Tokenをログに出力しない
- .envファイルをgitにコミットしない
