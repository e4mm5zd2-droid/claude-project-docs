# keihi-workspace

## 概要
経費管理ボットの作業用ワークスペース。Telegram経由で経費入力を受け付け、CSV形式で保存・月次集計を行う。

## 技術スタック
| カテゴリ | 技術 |
|---|---|
| AI | Claude Code（CLI） |
| データ | CSV（secretary/expenses/YYYY-MM.csv） |
| 定期実行 | cron（毎月1日 9:00 月次レポート） |
| デプロイ | Mac mini launchd (KeepAlive) |

## 機能（CLAUDE.mdより）
- **経費入力**: Telegram → CSV追記 → git push
- **カテゴリ**: 交通費, 消耗品, サーバー費, API費用, 外注費, 通信費, 広告費, その他
- **月次集計**: 毎月1日 9:00 自動実行

## データフロー
```
テラス/松本（Telegram）
  → 経費入力（金額・カテゴリ・備考）
  → secretary/expenses/YYYY-MM.csv に追記
  → git commit & push
  → 確認返信
```

## 現在の状態
- [ ] 開発中 / [x] 稼働中 / [ ] 停止中

## 関連事業
統括
