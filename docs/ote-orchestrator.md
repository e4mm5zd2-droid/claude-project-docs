# ote-orchestrator

株式会社on the edgeの経営AI「KURODO」のオーケストレーション層。
4つのデータソースを統合し、毎朝のデイリーブリーフィングとアクション承認フローを自動化する。

## 機能

### デイリーブリーフィング（毎朝9:00）
1. **ai-intel収集**: Supabase（or ローカルフォールバック）から直近24hのScore8+記事
2. **経費収集**: Google Sheetsから当月経費・予算消化率
3. **タスク収集**: MASTER_TASKS.mdから期限超過・未回収タスク
4. **KPI収集**: 各事業のKPIデータ（将来拡張）
5. **Claude分析**: 4データを統合し推奨アクション生成
6. **Telegram送信**: テラス・松本にプッシュ通知（承認可能な提案付き）
7. **Discord送信**: #generalにアーカイブ

### 承認フロー
- テラスがTelegramで「承認1」→ 該当タスクをMASTER_TASKSに追加→git push
- 「却下2」→ 却下として記録
- 「修正1 〇〇に変更」→ 修正内容でタスク化

## セットアップ

```bash
cd /Users/on-the-edge/Projects/ote-orchestrator
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .envを編集して各キーを設定
```

## 実行

```bash
# 手動テスト
source venv/bin/activate
python -m jobs.daily_briefing

# cron登録
crontab -e
# 以下を追加:
# 0 9 * * * cd /Users/on-the-edge/Projects/ote-orchestrator && /Users/on-the-edge/Projects/ote-orchestrator/venv/bin/python -m jobs.daily_briefing >> logs/daily_briefing.log 2>&1
```
