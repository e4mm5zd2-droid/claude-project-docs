# terrace-sokatsu-bot

## 概要
テラス用統括Telegram Bot。launchd（KeepAlive）で常時稼働し、テラスからのTelegramメッセージを受けてClaude Codeで経営関連タスクを実行する。

## 技術スタック
| カテゴリ | 技術 |
|---|---|
| 言語 | Bash / シェルスクリプト |
| Bot | Telegram Bot API |
| AI | Claude Code（CLI） |
| デプロイ | Mac mini launchd (KeepAlive) + cron healthcheck |

## アーキテクチャ
```
terrace-sokatsu-bot/
├── bot.py           # Telegram Botメインスクリプト
├── start.sh         # 起動スクリプト
└── healthcheck.sh   # 死活監視（cron 15分間隔）
```

## データフロー
```
テラス（Telegram）
  → terrace-sokatsu-bot (bot.py)
  → Claude Code起動（REPO_DIR=claude-project-docs）
  → ファイル操作・git push
  → Telegram返信
```

## 起動方法
```bash
# launchdが自動起動（KeepAlive）
# 手動: ./start.sh
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
