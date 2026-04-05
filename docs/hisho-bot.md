# hisho-bot

## 概要
HISHO Telegram Bot。Telegram経由でClaude Codeを操作し、秘書AI業務（タスク管理、リサーチ、議事録整理、未回収タスク催促）を実行する。KURODOとは異なり、経営判断ではなく執行管理に特化。

## 技術スタック
| カテゴリ | 技術 |
|---|---|
| 言語 | Bash / シェルスクリプト |
| Bot | Telegram Bot API |
| AI | Claude Code（CLI） |
| デプロイ | Mac mini tmux + cron healthcheck（15分間隔） |

## アーキテクチャ
```
hisho-bot/
├── bot.py           # Telegram Botメインスクリプト
├── start.sh         # 起動スクリプト
└── healthcheck.sh   # 死活監視（cron 15分間隔）
```

## データフロー
```
テラス/松本（Telegram）
  → hisho-bot (bot.py)
  → Claude Code起動（REPO_DIR=claude-project-docs）
  → タスク管理・リサーチ・議事録作成
  → Telegram返信
```

## 起動方法
```bash
./start.sh
```

### 環境変数（キー名のみ）
- TELEGRAM_BOT_TOKEN
- ALLOWED_USER_IDS
- REPO_DIR
- CLAUDE_PATH

## 現在の状態
- [ ] 開発中 / [x] 稼働中 / [ ] 停止中

## 関連事業
統括
