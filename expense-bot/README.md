# OTE 経費管理ボット

株式会社 on the edge の全社経費管理Telegramボット。
領収書の写真を送信するだけで、AIが自動解析 → 勘定科目分類 → Google Sheetsに記録。

## セットアップ

```bash
# 依存パッケージインストール
pip install -r requirements.txt

# 環境変数を設定
cp .env.example .env
# .env を編集して各キーを設定
```

### 必要な外部設定

1. **Telegram Bot** - @BotFather で作成しトークンを取得
2. **Anthropic API** - Claude APIキーを取得
3. **Google Sheets API** - サービスアカウント作成、スプレッドシートに共有設定

## 起動

```bash
python main.py
```

## 使い方

| 操作 | 方法 |
|------|------|
| 領収書登録 | 写真を送信 |
| テキスト登録 | `交通費 梅田→京都 560円 事業3` |
| 月次レポート | `/report` or `/report 2026/03` |
| 修正 | 登録直後に `2 5000`（金額を5000円に修正） |
| 確定 | `OK` |

## 技術スタック

- Python 3.11+ / python-telegram-bot v21
- Anthropic Claude API (Vision)
- Google Sheets API (gspread)
- Mac Mini常時稼働 (Polling方式)
