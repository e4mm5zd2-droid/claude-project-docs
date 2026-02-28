# X Auto Bot - 暗号通貨監視・自動投稿ボット

> X (Twitter) 自動投稿ボット。Claude AIで暗号通貨ニュースを監視・要約し自動投稿

*最終更新: 2026-02-28 19:21*

**パス**: `/Users/apple/Projects/business2-x-tools/x-auto-bot`
**ブランチ**: `main`

---
## README.md

# X（旧Twitter）自動投稿ボット

Anthropic API (Claude) を使って投稿文を自動生成し、X（旧Twitter）に投稿するPythonボットです。

## 機能

- Claude が AIやテクノロジーに関する投稿文を自動生成
- 生成した文章を自動でXに投稿
- 複数アカウント対応
- **🆕 画像付き自動投稿** - Cloudflare R2から画像を取得して投稿
- Web管理画面（OAuth 2.0認証）
- ターゲットツイート取得バッチ処理
- **🆕 暗号通貨アカウント監視機能** - 指定アカウントを監視してDiscord通知
- **🆕 Renderクラウド対応** - Cron Jobで定期実行

---

## フォルダ構造

```
x-auto-bot/
├── .env                 # 全認証情報
├── requirements.txt     # 依存関係
├── render.yaml          # 🆕 Render設定
├── README.md
│
├── bot/                 # 自動投稿機能
│   ├── main.py          # 単一アカウント投稿
│   ├── main_multi.py    # 複数アカウント投稿
│   └── accounts.json    # アカウント設定
│
├── crypto_bot/          # 🆕 暗号通貨監視ボット
│   ├── cron_monitor_bot.py       # Cron Job用（Render）
│   ├── auto_monitor_bot.py       # 自動版（ローカル）
│   └── simple_manual_bot.py      # 手動版（API制限回避）
│
├── web/                 # Web管理画面
│   ├── app.py           # Flask Webアプリ
│   ├── models.py        # DBモデル
│   ├── config.py        # ターゲット設定
│   └── fetch_and_process.py  # バッチ処理
│
├── scripts/             # ユーティリティ
│   ├── auth.py          # PIN認証（トークン取得）
│   └── get_user_id.py   # ユーザーID取得
│
├── docs/                # 🆕 ドキュメント
│   └── RENDER_DEPLOY_GUIDE.md  # Renderデプロイガイド
│
├── data/                # データベース・処理済みID（自動生成）
└── logs/                # ログファイル（自動生成）
```

---

## クイックスタート

### 1. 仮想環境のセットアップ

```bash
cd /Users/apple/Projects/x-auto-bot

# 仮想環境を有効化
source venv/bin/activate

# ライブラリをインストール（初回のみ）
pip install -r requirements.txt
```

### 2. 環境変数の確認

`.env` ファイルに以下が設定されていることを確認：

| 項目 | 用途 |
|------|------|
| `ANTHROPIC_API_KEY` | Claude API |
| `X_CONSUMER_KEY`, `X_CONSUMER_SECRET` | X API Consumer Keys |
| `DEVELOPER_ACCESS_TOKEN`, `DEVELOPER_ACCESS_TOKEN_SECRET` | X API Developer トークン（読み取り用） |
| `BOT_B_ACCESS_TOKEN`, `BOT_B_ACCESS_SECRET` | X API Bot トークン（投稿用） |
| `X_CLIENT_ID`, `X_CLIENT_SECRET` | X API (OAuth 2.0) |
| `DISCORD_WEBHOOK_URL` | 🆕 Discord通知用 Webhook URL |

---

## 実行コマンド一覧

```bash
# プロジェクトルートに移動
cd /Users/apple/Projects/x-auto-bot

# 仮想環境を有効化（毎回必要）
source venv/bin/activate
```

### Web管理画面

```bash
python web/app.py
# → http://127.0.0.1:5000 でアクセス
```

### 自動投稿ボット

```bash
# 単一アカウント
python bot/main.py

# 複数アカウント
python bot/main_multi.py

# 複数アカウント（一覧表示）
python bot/main_multi.py --list

# 複数アカウント（特定アカウントのみ）
python bot/main_multi.py --account アカウント名
```

### バッチ処理

```bash
# ターゲットツイート取得
python web/fetch_and_process.py
```

### 🆕 暗号通貨監視ボット

```bash
# 監視実行（Cron Job用 - 非対話型）
python crypto_bot/cron_monitor_bot.py

# 監視実行（自動版 - API権限必要）
python crypto_bot/auto_monitor_bot.py

# 手動リライト（API権限不要）
python crypto_bot/simple_manual_bot.py
```

### 🆕 画像付き自動投稿

`bot/accounts.json` で画像設定：

```json
{
  "name": "アカウント名",
  "image_mode": "fixed",
  "image_url": "https://your-bucket.r2.dev/images/image.jpg"
}
```

詳細は [docs/CLOUDFLARE_R2_SETUP.md](docs/CLOUDFLARE_R2_SETUP.md) を参照

### ユーティリティ

```bash
# ユーザーID取得
python scripts/get_user_id.py elonmusk Twitter

# PIN認証（他アカウントのトークン取得）
python scripts/auth.py
```

---

## 定期実行の設定（launchd）

### 単一アカウント（1日1回）

```bash
launchctl load ~/Library/LaunchAgents/com.user.xautobot.plist
```

### 複数アカウント（1日5回）

```bash
launchctl load ~/Library/LaunchAgents/com.user.xautobot.multi.plist
```

### 停止

```bash
launchctl unload ~/Library/LaunchAgents/com.user.xautobot.plist
launchctl unload ~/Library/LaunchAgents/com.user.xautobot.multi.plist
```

---

## 🆕 Renderクラウドデプロイ

監視ボットをRenderで定期実行する場合：

```bash
# GitHubリポジトリ作成
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/x-auto-bot.git
git push -u origin main
```

詳細は [docs/RENDER_DEPLOY_GUIDE.md](docs/RENDER_DEPLOY_GUIDE.md) を参照。

---

## トラブルシューティング

### 自動投稿ボット

#### 「ANTHROPIC_API_KEYが設定されていません」

→ `.env` ファイルに `ANTHROPIC_API_KEY` が正しく設定されているか確認

#### 「403 Forbidden」エラー

→ X Developer Portal でアプリの権限が「読み取りと書き込み」になっているか確認
→ Access Token を再生成

#### 「Missing valid authorization header」

→ X Developer Portal で Client Secret を再生成し、`.env` を更新

### 🆕 暗号通貨監視ボット

#### 「403 Forbidden (Error 453)」エラー

→ X APIの従量課金がまだアクティブ化されていない
→ クレジット購入後24-48時間待機、または投稿を行いクレジット消費

#### Discord通知が届かない

→ `DISCORD_WEBHOOK_URL` が正しく設定されているか確認
→ Discord Webhookが削除されていないか確認

#### 重複ツイートが処理される

→ `data/processed_tweets.txt` を削除して再実行

### その他

#### 仮想環境を抜ける

```bash
deactivate
```

---

## ログファイル

| ファイル | 内容 |
|----------|------|
| `logs/bot.log` | 単一アカウント投稿ログ |
| `logs/bot_multi.log` | 複数アカウント投稿ログ |
| `logs/fetch_batch.log` | バッチ処理ログ |
| `logs/cron_monitor_bot.log` | 🆕 暗号通貨監視ボットログ |

---

## 設定ファイル

| ファイル | 内容 |
|----------|------|
| `.env` | API認証情報 |
| `bot/accounts.json` | 複数アカウント設定 |
| `web/config.py` | ターゲット監視設定 |


---
## CLAUDE.md

# Project Instructions for Claude

For every project, write a detailed FORapple.md file that explains the whole project in plain language.


---
## 技術スタック


### Python Dependencies

```
tweepy
anthropic
python-dotenv
requests
Flask>=3.0.0
gunicorn>=21.2.0
SQLAlchemy>=2.0.0
psycopg2-binary>=2.9.9
```

---
## ディレクトリ構成

```
├── bot/
│   ├── accounts.json
│   ├── accounts.json.example
│   ├── main.py
│   └── main_multi.py
├── crypto_bot/
│   ├── QUICKSTART.md
│   ├── QUICKSTART_quote.md
│   ├── README_discord_bot.md
│   ├── README_monitoring.md
│   ├── README_quote_tweet.md
│   ├── auto_crypto_expert.py
│   ├── auto_monitor_bot.py
│   ├── auto_monitoring_bot.py
│   ├── auto_post_monitor_bot.py
│   ├── auto_quote_monitor.py
│   ├── com.user.crypto_monitoring_bot.plist
│   ├── cron_monitor_bot.py
│   ├── discord_notification_bot.py
│   ├── manual_rewrite_bot.py
│   ├── quote_tweet.py
│   ├── setup_scheduler.sh
│   └── simple_manual_bot.py
├── docs/
│   ├── CLAUDE_PROJECT_SETUP.md
│   ├── CLOUDFLARE_R2_SETUP.md
│   ├── DIRECTORY_STRUCTURE.md
│   └── RENDER_DEPLOY_GUIDE.md
├── scripts/
│   ├── activate_api.py
│   ├── auth.py
│   ├── check_following.py
│   ├── find_crypto_tweet.py
│   ├── follow_targets.py
│   ├── get_bot_token.py
│   ├── get_token_with_verifier.py
│   ├── get_user_id.py
│   ├── test_auth.py
│   ├── test_developer_auth.py
│   └── tokens.txt
├── web/
│   ├── .claude/
│   │   └── settings.local.json
│   ├── README.md
│   ├── app.py
│   ├── config.py
│   ├── fetch_and_process.py
│   ├── models.py
│   └── users.db
├── .env.example
├── .gitignore
├── CLAUDE.md
├── Procfile
├── README.md
├── com.user.auto_quote_monitor.plist
├── com.user.xautobot.multi.plist
├── com.user.xautobot.plist
├── launchd.log
├── launchd_error.log
├── launchd_multi.log
├── launchd_multi_error.log
├── render.yaml
└── requirements.txt
```

---
## デプロイ設定 (render.yaml)

```yaml
# ===========================================
# Render デプロイ設定ファイル
# ===========================================
# 削除済みサービス（コードはGitHubに残存）:
#   - x-auto-bot-web (web/app.py) - 顧客管理Web画面
#   - x-auto-bot-db (PostgreSQL) - 顧客トークンDB
#   - crypto-monitor-bot (crypto_bot/cron_monitor_bot.py) - Discord通知Bot

services:
  # 自動引用投稿ボット（2時間ごと、最大4件）
  - type: cron
    name: crypto-auto-quote-bot
    runtime: python
    plan: starter
    schedule: "0 */2 * * *"  # 2時間ごとに実行
    buildCommand: pip install -r requirements.txt
    startCommand: python3 crypto_bot/auto_quote_monitor.py --limit 4 --hours 2
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: X_BEARER_TOKEN
        sync: false
      - key: X_CONSUMER_KEY
        sync: false
      - key: X_CONSUMER_SECRET
        sync: false
      - key: DEVELOPER_ACCESS_TOKEN
        sync: false
      - key: DEVELOPER_ACCESS_TOKEN_SECRET
        sync: false
      - key: X_ACCESS_TOKEN
        sync: false
      - key: X_ACCESS_TOKEN_SECRET
        sync: false

```

---
## プロジェクトドキュメント


### docs/CLAUDE_PROJECT_SETUP.md

# Claude Project 設定ガイド - 事業2（Xツール販売）

## 概要

このドキュメントは、事業2（Xツール販売）の営業戦略・価格設計・販売準備のために、Claude Projectに登録すべきファイルとキックオフプロンプトを定義します。

---

## 📁 Project登録ファイル - 優先度順

### **Tier 1: 経営方針・組織情報・プロジェクト構造（必須）**

プロジェクトの最優先コンテキスト。Projectの基礎となる意思決定構造。

| 優先度 | ファイル | 理由 |
|-------|---------|------|
| ★★★★★ | `.cursor/rules/kurodo-統括セッション.mdc` | 会社全体の経営方針・意思決定ルール・KURODO定義 |
| ★★★★★ | `.cursor/rules/kurodo-事業2-xツール販売.mdc` | 事業2の戦略・価格設計・競合分析・KPI |
| ★★★★★ | `docs/DIRECTORY_STRUCTURE.md` | プロジェクト構造・ファイル配置・依存関係 |

**登録方法:**
- Claude Project設定 → "Project Knowledge" → "Add Files"
- 上記3ファイルをアップロード

---

### **Tier 2: プロダクト仕様・技術情報（重要）**

営業資料作成・価格設計・機能説明に必要な技術コンテキスト。

| 優先度 | ファイル | 理由 |
|-------|---------|------|
| ★★★★☆ | `README.md` | プロダクト全体の機能概要・フォルダ構造 |
| ★★★★☆ | `bot/main.py` | 自動投稿の実装（主要機能） |
| ★★★☆☆ | `web/app.py` | Web管理画面の実装（OAuth認証・UI） |
| ★★★☆☆ | `render.yaml` | デプロイ構成・本番環境設定 |
| ★★★☆☆ | `docs/RENDER_DEPLOY_GUIDE.md` | 運用ガイド・コスト情報 |

**登録方法:**
- 上記ファイルをProjectに追加
- 技術的質問（「予約投稿機能の実装状況は？」等）に即答可能になる

---

### **Tier 3: 営業資料・戦略ドキュメント（これから作成）**

営業活動に直接使用する資料。Projectに追加することで継続的にブラッシュアップ可能。

| 優先度 | ファイル（予定） | 理由 |
|-------|-----------------|------|
| ★★★★★ | `docs/SALES_PITCH.md` | 営業トークスクリプト・価格表・FAQ |
| ★★★★☆ | `docs/LANDING_PAGE_DRAFT.md` | LP構成案・訴求メッセージ |
| ★★★☆☆ | `docs/COMPETITIVE_ANALYSIS.md` | 競合詳細分析（SocialDog等） |
| ★★☆☆☆ | `docs/CUSTOMER_CASE_STUDIES.md` | 導入事例（獲得後に追加） |

**作成タイミング:**
- 今週中に `SALES_PITCH.md` と `LANDING_PAGE_DRAFT.md` を作成
- Projectに追加後、Claude と継続的にブラッシュアップ

---

## 🚀 キックオフ・プロンプト（Project Instructions）

以下をClaude Projectの **"Custom Instructions"** に設定してください。

```markdown
# KURODO 事業2（Xツール販売）専用AI v1.0

## IDENTITY

あなたは「KURODO」。株式会社 on the edge の経営パートナーAI。
このProjectでは事業2（Xツール販売）に特化して機能する。

**兼任役職：**
- CEO（最高経営責任者）：全体戦略・最終意思決定
- COO（最高執行責任者）：営業戦略・実行計画・タスク設計
- CTO（最高技術責任者）：技術仕様・開発ロードマップ
- CMO（最高マーケティング責任者）：価格設計・競合分析・販売戦略

**ペルソナ：**
- 論理的・多角的・冷静
- 全発言は事実ベース・数字ベース
- 勝機を検出した場合、大胆かつ攻撃的な提案を躊躇なく行う
- 聞かれていなくても能動的に警告・提案する

**禁止：**
- 感情的な励まし（「頑張りましょう」「素晴らしい」等）
- 曖曧な表現
- 判断の回避
- 抽象論のみの回答
- 「いかがでしょうか？」で終わる回答

---

## 組織構造

**意思決定者：**
- テラス孝之（代表取締役）：営業・交渉・最終承認
- 松本：開発・技術実装
- KURODO（あなた）：戦略・判断・タスク設計

**意思決定ルール：**
- 最終意思決定者はテラス孝之
- 技術的判断はCTOの見解を重視
- KURODOは判断を断言する（「どうしますか？」で終わるな）

---

## プロダクト情報

**名称：** X 自動投稿ツール（仮称）

**現在の機能：**
- 自動投稿（Claude生成 → X投稿）
- 投稿スケジュール（1日の回数・時間指定）
- 予約投稿（若干の難点あり・要修正）
- Web管理画面（OAuth 2.0認証・複数アカウント管理）
- データベース（PostgreSQL・アカウント情報保存）

**技術スタック：**
- Python 3.11
- Flask（Web管理画面）
- Tweepy（X API）
- Anthropic API（Claude Sonnet 4）
- PostgreSQL（Render）

**開発完成度：** 95%（予約投稿修正のみ残）

---

## 販売戦略

**ターゲット顧客：**
1. 個人インフルエンサー・アフィリエイター
2. 小規模事業者（SNS担当者不在）
3. 中小企業

**価格帯（提案）：**
- ライト：¥49,800/月
- スタンダード：¥98,000/月
- プレミアム：¥198,000/月
- エンタープライズ：応相談

**販売チャネル：**
- 主力：営業代行（成果報酬型・売上の30%）
- 補助：自社X告知・LP

**競合：**
- SocialDog（AI生成なし）
- Hootsuite（高額・日本語弱い）
- Hypefury（日本語最適化弱い）

**差別化ポイント：**
- AI自動生成＋自動投稿のワンストップ
- 日本語完全対応
- 140〜5,000字の柔軟な文字数設定

---

## 月商500万円への貢献目標

**3ヶ月後（5月11日）：**
- 成約社数：20社
- 平均単価：¥125,000/月
- MRR（月間定期収益）：¥2,500,000
- 事業2の貢献度：50%（250万円）

---

## 出力フォーマット

**相談・提案時：**

```
【KURODO 事業2判断】
結論：[断言]
判断理由：[2-3行]

【CTO分析】[技術/開発/実装]
【CMO分析】[市場/競合/価格/販売]
【COO分析】[実行計画/営業代行/担当割振り]

【今日やること】
□ テラス：[タスク / 完了条件]
□ 松本：[タスク / 完了条件]

【今週やること】
□ [タスク]（担当/期限）
```

**冒頭サマリー（毎回）：**

```
【事業2サマリー】YYYY/MM/DD
プロダクト完成度：95%
営業代行：○名稼働 / アポ：○件 / 成約：○件
MRR：¥○○
最優先：[内容]
```

---

## 行動原則

1. **利益最大化が最上位**
2. **即日実行が絶対原則**
3. **日次PDCA・走りながら修正**
4. **グレーな手法は法の範囲内で積極採用**
5. **出力は長くてよい。全分析を出せ**
6. **競合は実名で分析**

---

## 現在のフェーズ

**日付：** 2026年2月11日
**ステータス：** プロダクト完成・Renderデプロイ成功
**次のステップ：** 営業資料作成 → 営業代行選定 → 営業開始

---

## あなた（KURODO）に期待すること

1. **営業資料の作成支援**
   - 営業トークスクリプト
   - LP構成案
   - 競合比較表
   - FAQ

2. **価格戦略の最適化**
   - 市場調査
   - 顧客セグメント別の価格設定
   - 成果報酬型営業代行の報酬率設計

3. **営業代行の選定基準設計**
   - 募集文面
   - 選定基準
   - 契約条件

4. **技術的課題の特定**
   - 予約投稿の難点解決
   - スケーラビリティ検証
   - ユーザーダッシュボードの必要性判断

5. **売上シミュレーション**
   - 保守的・標準・攻撃的シナリオ
   - KPI設計
   - 週次レポート

---

## 対話開始時のデフォルト動作

ユーザーが相談を開始したら、以下を自動実行：

1. **冒頭サマリーを表示**（日付・プロダクト完成度・MRR・最優先事項）
2. **相談内容を4役職の視点で分析**（CEO/COO/CTO/CMO）
3. **具体的なアクションプランを提示**（今日やること・今週やること）
4. **数字で判断**（売上インパクト・ROI・実行速度）

---

## 禁止事項（再確認）

- 感情的表現
- 抽象論だけの回答
- 「いかがでしょうか？」で終わる回答
- 情報不足を理由に回答拒否（仮説で回答し不足点を指定）
- 今日実行できることを含まない提案
- 事業レベルの撤退提案
- 「リスクがあるのでやめましょう」という守りの提案

---

## 成功の定義

**短期（1ヶ月）：**
- 営業代行3名稼働
- 成約3社
- MRR：¥300,000

**中期（3ヶ月）：**
- 営業代行5名稼働
- 成約20社
- MRR：¥2,500,000

**長期（6ヶ月）：**
- 営業代行10名稼働
- 成約50社
- MRR：¥6,000,000
- 月商500万円の中核事業として確立

---

以上。今すぐ戦いを始めよう。
```

---

## 📝 Project作成手順

### 1. Claude Projectを作成

1. Claude.ai にアクセス
2. 左サイドバー → **"Projects"** → **"New Project"**
3. プロジェクト名：**事業2 - Xツール販売**

### 2. Custom Instructionsを設定

1. Project設定 → **"Project Instructions"**
2. 上記の「キックオフ・プロンプト」を全文コピペ
3. 保存

### 3. Knowledgeファイルを追加

**Tier 1（必須）：**
- `.cursor/rules/kurodo-統括セッション.mdc`
- `.cursor/rules/kurodo-事業2-xツール販売.mdc`

**Tier 2（推奨）：**
- `README.md`
- `bot/main.py`
- `web/app.py`
- `render.yaml`

### 4. 最初の対話を開始

Projectを開いて以下を入力：

```
営業資料を作成したい。以下を今日中に作成する：
1. 営業トークスクリプト（A4 1枚）
2. LP構成案（1枚もの）
3. 競合比較表

まずは営業トークスクリプトから作成してください。
```

---

## 🎯 期待される効果

**Before（Projectなし）：**
- 相談のたびに会社情報・プロダクト仕様を説明
- 回答が抽象的・感情的
- 技術的コンテキストが不足
- 一貫性のない判断

**After（Project設定済み）：**
- ✅ 会社情報・経営方針を記憶
- ✅ プロダクト仕様を即座に参照
- ✅ 4役職の視点で多角的分析
- ✅ 数字ベースの具体的判断
- ✅ 今日やること・今週やることを即座に提示

---

## 🔄 継続的改善

**営業資料完成後：**
1. `docs/SALES_PITCH.md` を作成
2. Projectに追加
3. 実際の営業で得たフィードバックを反映
4. Claudeと継続的にブラッシュアップ

**成約獲得後：**
1. `docs/CUSTOMER_CASE_STUDIES.md` を作成
2. 導入事例を蓄積
3. 営業資料に追加

**競合分析更新：**
1. 競合の価格変更・新機能をキャッチ
2. `docs/COMPETITIVE_ANALYSIS.md` を更新
3. 差別化ポイントを再定義

---

## 📊 Project効果測定

| 指標 | 目標 | 測定方法 |
|-----|------|---------|
| 相談→回答の速度 | 2分以内 | 主観評価 |
| 回答の具体性 | アクションプラン含有率100% | 主観評価 |
| 営業資料作成速度 | 1日以内 | 実測 |
| 戦略の一貫性 | 矛盾ゼロ | 主観評価 |

---

**作成日：** 2026年2月11日  
**作成者：** KURODO（Claude Sonnet 4）  
**バージョン：** 1.0


### docs/CLOUDFLARE_R2_SETUP.md

# Cloudflare R2 画像ストレージ セットアップガイド

画像付き自動投稿のためのCloudflare R2の設定方法

## 📦 Cloudflare R2とは

- Amazon S3互換のオブジェクトストレージ
- **無料枠**: 10GB
- **料金**: 超過後も格安（$0.015/GB/月）
- **転送料金**: 無料
- **速度**: 高速

## 🚀 セットアップ手順

### 1. Cloudflareアカウント作成

1. [Cloudflare](https://www.cloudflare.com) にアクセス
2. 「Sign Up」でアカウント作成（無料）
3. メール認証を完了

### 2. R2バケット作成

1. ダッシュボードで **R2** を選択
2. **Create bucket** をクリック
3. バケット名を入力（例: `x-auto-bot-images`）
4. リージョンを選択（推奨: Asia Pacific）
5. **Create bucket** をクリック

### 3. 公開アクセスを有効化

1. 作成したバケットを開く
2. **Settings** タブをクリック
3. **Public access** セクションで以下を設定：
   - **Allow Public Access**: ON
   - **Custom domain** を設定（例: `images.yourdomain.com`）
   - または **R2.dev subdomain** を有効化
4. **Save** をクリック

### 4. 画像をアップロード

#### 方法1: Web UIでアップロード

1. バケットの **Objects** タブを開く
2. **Upload** をクリック
3. 画像ファイルを選択（JPG, PNG, GIF対応）
4. フォルダ構造を作成可能（例: `images/account1.jpg`）

#### 方法2: Wranglerコマンドでアップロード

```bash
# Wranglerをインストール
npm install -g wrangler

# 認証
wrangler login

# 画像をアップロード
wrangler r2 object put x-auto-bot-images/images/account1.jpg --file=./account1.jpg
```

### 5. 画像URLを取得

アップロード後、画像のURLは以下の形式になります：

```
https://your-bucket-name.r2.dev/images/account1.jpg
```

または、カスタムドメインを設定した場合：

```
https://images.yourdomain.com/account1.jpg
```

## 📝 accounts.json への設定

### 固定画像の場合

```json
{
  "name": "@_31celsior",
  "image_mode": "fixed",
  "image_url": "https://your-bucket.r2.dev/images/account1.jpg"
}
```

### ランダム画像の場合

```json
{
  "name": "@crypto_0101010",
  "image_mode": "random",
  "image_urls": [
    "https://your-bucket.r2.dev/images/crypto1.jpg",
    "https://your-bucket.r2.dev/images/crypto2.jpg",
    "https://your-bucket.r2.dev/images/crypto3.jpg"
  ]
}
```

### 画像なしの場合

```json
{
  "name": "@text_only",
  "image_mode": "none"
}
```

## 🎨 画像の推奨仕様

| 項目 | 推奨値 |
|-----|-------|
| **形式** | JPG, PNG |
| **サイズ** | 1200x675px（16:9） |
| **最大サイズ** | 5MB以下 |
| **アスペクト比** | 16:9, 4:3, 1:1 |

Xでの最適な表示のため、**1200x675px (16:9)** を推奨します。

## 💰 料金目安

| 使用量 | 月額料金 |
|-------|---------|
| 10GB以下 | **$0**（無料） |
| 50GB | 約$0.60 |
| 100GB | 約$1.35 |

**転送料金は無料**なので、何回アクセスされても追加料金なし。

## 🔧 トラブルシューティング

### 画像が表示されない

1. **Public access** が有効になっているか確認
2. URLが正しいか確認（ブラウザで直接開いてみる）
3. CORSエラーの場合、バケット設定でCORSを有効化

### アップロードできない

1. ファイルサイズが5MB以下か確認
2. ファイル名に日本語や特殊文字が含まれていないか確認
3. Cloudflareアカウントの支払い方法が登録されているか確認

## 📚 参考リンク

- [Cloudflare R2 公式ドキュメント](https://developers.cloudflare.com/r2/)
- [R2 料金](https://developers.cloudflare.com/r2/pricing/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)


### docs/DIRECTORY_STRUCTURE.md

# X自動投稿ツール - ディレクトリ構造

**プロジェクト名:** x-auto-bot  
**バージョン:** 1.0  
**最終更新:** 2026年2月11日

---

## 📂 完全なディレクトリツリー

```
x-auto-bot/
├── .env                          # 🔐 環境変数（全認証情報）
├── .env.example                  # 環境変数のテンプレート
├── .gitignore                    # Git除外設定
├── requirements.txt              # Python依存関係
├── Procfile                      # Heroku用設定（現在未使用）
├── render.yaml                   # ⚙️ Render デプロイ設定
├── README.md                     # プロジェクト概要
├── CLAUDE.md                     # Claude連携メモ
│
├── bot/                          # 🤖 自動投稿機能（メインプロダクト）
│   ├── main.py                   # ★ 単一アカウント自動投稿
│   ├── main_multi.py             # ★ 複数アカウント自動投稿
│   ├── accounts.json             # アカウント設定（Git除外）
│   └── accounts.json.example     # アカウント設定テンプレート
│
├── crypto_bot/                   # 💰 暗号通貨監視ボット
│   ├── cron_monitor_bot.py       # ★ Cron Job用（Render本番環境）
│   ├── auto_monitor_bot.py       # 自動版（API権限必要）
│   ├── auto_monitoring_bot.py    # 自動監視（旧版）
│   ├── auto_post_monitor_bot.py  # 監視→自動投稿版
│   ├── auto_crypto_expert.py     # 暗号通貨専門家Bot
│   ├── simple_manual_bot.py      # 手動版（API制限回避）
│   ├── manual_rewrite_bot.py     # 手動リライト版
│   ├── discord_notification_bot.py # Discord通知専用
│   ├── quote_tweet.py            # 引用ツイート機能
│   ├── setup_scheduler.sh        # スケジューラー設定スクリプト
│   ├── QUICKSTART.md             # クイックスタートガイド
│   ├── QUICKSTART_quote.md       # 引用ツイートガイド
│   ├── README_discord_bot.md     # Discord Bot説明
│   ├── README_monitoring.md      # 監視機能説明
│   └── README_quote_tweet.md     # 引用ツイート説明
│
├── web/                          # 🌐 Web管理画面（Flask）
│   ├── app.py                    # ★ Flask Webアプリ（OAuth 2.0）
│   ├── models.py                 # ★ SQLAlchemyモデル（PostgreSQL/SQLite）
│   ├── config.py                 # ターゲット設定
│   ├── fetch_and_process.py      # バッチ処理（ツイート取得）
│   └── README.md                 # Web機能説明
│
├── scripts/                      # 🛠️ ユーティリティスクリプト
│   ├── auth.py                   # PIN認証（トークン取得）
│   ├── get_user_id.py            # ユーザーID取得
│   ├── get_bot_token.py          # Bot トークン取得
│   ├── get_token_with_verifier.py # OAuth 2.0トークン取得
│   ├── test_auth.py              # 認証テスト
│   ├── test_developer_auth.py    # Developer認証テスト
│   ├── activate_api.py           # API有効化スクリプト
│   ├── check_following.py        # フォロー状態確認
│   ├── follow_targets.py         # ターゲットフォロー
│   └── find_crypto_tweet.py      # 暗号通貨ツイート検索
│
├── docs/                         # 📚 ドキュメント
│   ├── RENDER_DEPLOY_GUIDE.md    # Renderデプロイガイド
│   ├── CLOUDFLARE_R2_SETUP.md    # Cloudflare R2 画像設定
│   ├── CLAUDE_PROJECT_SETUP.md   # Claude Project設定ガイド
│   └── DIRECTORY_STRUCTURE.md    # ★ このファイル
│
├── data/                         # 📊 データベース・処理済みID
│   ├── .gitkeep                  # 空ディレクトリ保持用
│   ├── users.db                  # SQLite DB（ローカル開発用）
│   └── processed_tweets.txt      # 処理済みツイートID
│
└── logs/                         # 📝 ログファイル（自動生成）
    ├── bot.log                   # 単一アカウント投稿ログ
    ├── bot_multi.log             # 複数アカウント投稿ログ
    ├── fetch_batch.log           # バッチ処理ログ
    └── cron_monitor_bot.log      # 暗号通貨監視ボットログ
```

---

## 📁 ディレクトリ詳細説明

### **1. ルートディレクトリ**

| ファイル | 役割 | 重要度 |
|---------|------|--------|
| `.env` | 全認証情報（Anthropic API、X API、Discord Webhook等） | ★★★★★ |
| `requirements.txt` | Python依存関係（Flask、tweepy、anthropic等） | ★★★★★ |
| `render.yaml` | Renderデプロイ設定（Web/Cron Job/DB） | ★★★★☆ |
| `README.md` | プロジェクト概要・使い方 | ★★★★☆ |

---

### **2. bot/ - 自動投稿機能（メインプロダクト）**

**役割:** X（旧Twitter）への自動投稿を実行する中核機能。

| ファイル | 機能 | 実行方法 |
|---------|------|---------|
| `main.py` | 単一アカウントで自動投稿 | `python bot/main.py` |
| `main_multi.py` | 複数アカウントで自動投稿 | `python bot/main_multi.py` |
| `accounts.json` | アカウント設定（トピック・プロンプト・画像URL） | 手動編集 |

**技術スタック:**
- Anthropic API（Claude Sonnet 4）：投稿文生成
- Tweepy（X API v2）：投稿実行
- Cloudflare R2：画像取得（オプション）

**販売対象機能:** この部分が顧客に提供する主要機能

---

### **3. crypto_bot/ - 暗号通貨監視ボット**

**役割:** 暗号通貨アカウントを監視し、リライトしてDiscord通知。

| ファイル | 用途 | 環境 |
|---------|------|------|
| `cron_monitor_bot.py` | **本番環境用**（Render Cron Job） | 本番 |
| `auto_monitor_bot.py` | 自動監視（API権限必要） | ローカル |
| `simple_manual_bot.py` | 手動入力版（API制限回避） | ローカル |
| `auto_post_monitor_bot.py` | 監視→自動投稿版 | ローカル |

**監視対象アカウント（例）:**
- @coinlikecoin, @taka__crypto, @yousukeakaban, @grvt_io 等

**技術スタック:**
- X API v2（ユーザータイムライン取得）
- Anthropic API（リライト生成）
- Discord Webhook（通知送信）

**現在の状態:**
- Renderで定期実行中（毎時0分）
- API権限制限により一部機能制限あり

---

### **4. web/ - Web管理画面（Flask）**

**役割:** OAuth 2.0認証で複数アカウントを管理。

| ファイル | 役割 | 技術 |
|---------|------|------|
| `app.py` | Flask Webアプリ本体 | Flask、OAuth 2.0 |
| `models.py` | SQLAlchemyモデル（ユーザー管理） | SQLAlchemy、PostgreSQL/SQLite |
| `config.py` | ターゲット設定 | Python |
| `fetch_and_process.py` | バッチ処理（ツイート取得） | Tweepy |

**本番環境:**
- URL: `https://x-auto-bot-web.onrender.com/`
- データベース: PostgreSQL（Render）
- 認証: X OAuth 2.0（PKCE）

**ローカル開発:**
- データベース: SQLite（`data/users.db`）
- URL: `http://127.0.0.1:5000/`

**販売対象機能:** 顧客がアカウントを登録・管理するUI

---

### **5. scripts/ - ユーティリティスクリプト**

**役割:** 開発・テスト・認証用のヘルパースクリプト。

| カテゴリ | ファイル | 用途 |
|---------|---------|------|
| **認証** | `auth.py` | PIN認証（OAuth 1.0a） |
| | `get_bot_token.py` | Bot トークン取得 |
| | `test_auth.py` | 認証テスト |
| **API操作** | `activate_api.py` | API有効化 |
| | `get_user_id.py` | ユーザーID取得 |
| | `find_crypto_tweet.py` | ツイート検索 |
| **フォロー管理** | `check_following.py` | フォロー状態確認 |
| | `follow_targets.py` | 一括フォロー |

**使用頻度:** 開発時のみ（本番では未使用）

---

### **6. docs/ - ドキュメント**

| ファイル | 内容 | 対象読者 |
|---------|------|---------|
| `RENDER_DEPLOY_GUIDE.md` | Renderデプロイ手順 | 開発者 |
| `CLOUDFLARE_R2_SETUP.md` | 画像アップロード設定 | 開発者 |
| `CLAUDE_PROJECT_SETUP.md` | Claude Project設定 | 経営陣 |
| `DIRECTORY_STRUCTURE.md` | ディレクトリ構造説明（このファイル） | AI・開発者 |

---

### **7. data/ - データ保存**

**役割:** データベース・処理済みID・キャッシュ。

| ファイル | 内容 | 環境 |
|---------|------|------|
| `users.db` | SQLite DB（OAuth認証情報） | ローカル |
| `processed_tweets.txt` | 処理済みツイートID（重複防止） | 全環境 |

**Git除外:** `.gitignore` でコミット対象外

---

### **8. logs/ - ログファイル**

**役割:** 実行ログ・エラーログ。

| ファイル | 記録内容 |
|---------|---------|
| `bot.log` | 単一アカウント投稿ログ |
| `bot_multi.log` | 複数アカウント投稿ログ |
| `fetch_batch.log` | バッチ処理ログ |
| `cron_monitor_bot.log` | 監視ボットログ |

**Git除外:** `.gitignore` でコミット対象外

---

## 🔗 ファイル間の依存関係

### **主要な依存チェーン**

```
1. 自動投稿フロー
   bot/main.py
     └─ .env (ANTHROPIC_API_KEY, X_API_KEY等)
     └─ Anthropic API (投稿文生成)
     └─ Tweepy (X API投稿)
     └─ logs/bot.log (ログ出力)

2. 複数アカウント投稿フロー
   bot/main_multi.py
     └─ bot/accounts.json (アカウント設定)
     └─ .env (認証情報)
     └─ Cloudflare R2 (画像取得 - オプション)
     └─ logs/bot_multi.log

3. Web管理画面
   web/app.py
     └─ web/models.py (DBモデル)
     └─ .env (X_CLIENT_ID, X_CLIENT_SECRET等)
     └─ data/users.db (ローカル) or PostgreSQL (本番)

4. 暗号通貨監視ボット
   crypto_bot/cron_monitor_bot.py
     └─ .env (DISCORD_WEBHOOK_URL, ANTHROPIC_API_KEY)
     └─ data/processed_tweets.txt (重複防止)
     └─ Discord Webhook (通知)
```

---

## 🎯 重要ファイル TOP10（Claude Project登録推奨）

| 順位 | ファイル | 理由 |
|-----|---------|------|
| 1 | `README.md` | プロジェクト全体概要 |
| 2 | `bot/main.py` | メインプロダクト（自動投稿） |
| 3 | `bot/main_multi.py` | 複数アカウント対応 |
| 4 | `web/app.py` | Web管理画面（OAuth） |
| 5 | `web/models.py` | データベース設計 |
| 6 | `render.yaml` | デプロイ設定 |
| 7 | `requirements.txt` | 依存関係 |
| 8 | `crypto_bot/cron_monitor_bot.py` | 監視ボット本番版 |
| 9 | `docs/RENDER_DEPLOY_GUIDE.md` | 運用ガイド |
| 10 | `docs/DIRECTORY_STRUCTURE.md` | このファイル |

---

## 🚀 機能別ファイルマッピング

### **販売対象機能 → ファイル**

| 機能 | 実装ファイル | 完成度 |
|-----|------------|--------|
| 自動投稿 | `bot/main.py`, `bot/main_multi.py` | ✅ 100% |
| 投稿スケジュール | `bot/main_multi.py` (cron連携) | ✅ 100% |
| 予約投稿 | `bot/main_multi.py` (時刻指定) | ⚠️ 80%（若干の難点） |
| Web管理画面 | `web/app.py`, `web/models.py` | ✅ 100% |
| アカウント管理 | `web/models.py` (User モデル) | ✅ 100% |
| 画像付き投稿 | `bot/main_multi.py` + Cloudflare R2 | ✅ 100% |
| 分析機能 | 未実装 | 🔜 0% |

---

## 📊 コードベース統計

```
言語別ファイル数:
- Python: 25ファイル
- Markdown: 10ファイル
- 設定ファイル: 5ファイル

主要ファイルの行数（推定）:
- bot/main.py: ~180行
- bot/main_multi.py: ~350行
- web/app.py: ~360行
- web/models.py: ~140行
- crypto_bot/cron_monitor_bot.py: ~250行

総コード行数: 約2,500行（推定）
```

---

## 🔐 セキュリティ重要ファイル（Git除外）

以下は `.gitignore` で除外され、Gitにコミットされない：

```
.env                    # 全認証情報
bot/accounts.json       # アカウント設定
data/users.db           # SQLite DB
data/processed_tweets.txt
logs/*.log
__pycache__/
*.pyc
venv/
```

---

## 🛠️ 開発環境

```
仮想環境パス: /Users/apple/Projects/x-auto-bot/venv/
Python バージョン: 3.9+ (推奨: 3.11)
エディタ: Cursor (VSCode ベース)
```

**有効化コマンド:**
```bash
cd /Users/apple/Projects/x-auto-bot
source venv/bin/activate
```

---

## 📦 主要依存関係（requirements.txt）

```
tweepy                # X API（投稿・監視）
anthropic             # Claude API（文章生成）
python-dotenv         # 環境変数読み込み
requests              # HTTP通信
Flask>=3.0.0          # Web管理画面
gunicorn>=21.2.0      # 本番Webサーバー
SQLAlchemy>=2.0.0     # ORM（データベース）
psycopg2-binary>=2.9.9 # PostgreSQL接続
```

---

## 🌐 本番環境（Render）

**サービス構成:**

```
1. Web Service
   - 名前: x-auto-bot-web
   - URL: https://x-auto-bot-web.onrender.com/
   - コマンド: gunicorn web.app:app
   - ソース: web/app.py

2. Cron Job
   - 名前: crypto-monitor-bot
   - スケジュール: 毎時0分
   - コマンド: python3 crypto_bot/cron_monitor_bot.py

3. Database
   - 種類: PostgreSQL
   - プラン: Free
   - 接続: DATABASE_URL 環境変数
```

---

## 🎓 新規開発時のファイル配置ガイド

| 機能追加内容 | 配置先ディレクトリ | ファイル名例 |
|------------|-----------------|------------|
| 新しい投稿ロジック | `bot/` | `custom_post.py` |
| 新しい監視ボット | `crypto_bot/` | `new_monitor_bot.py` |
| Web機能追加 | `web/` | `new_feature.py` |
| ユーティリティ | `scripts/` | `helper_script.py` |
| ドキュメント | `docs/` | `NEW_GUIDE.md` |
| テスト | `tests/` (新規作成) | `test_*.py` |

---

## 🔄 バージョン管理

**Git リポジトリ:**
- GitHub: `https://github.com/e4mm5zd2-droid/x-auto-bot.git`
- ブランチ: `main`

**最近のコミット:**
- `198d537` - Fix Render deployment error: Add missing dependencies
- `6b7ac14` - Add image upload feature with Cloudflare R2 support
- `d3e404a` - Add auto-post monitoring bot for @crypto_0101010

---

## 📞 サポート情報

**プロジェクト責任者:**
- 代表: テラス孝之（照 隆行）
- 技術担当: 松本
- 戦略AI: KURODO（Claude Sonnet 4）

**問い合わせ:**
- 技術的質問: 松本
- 経営判断: テラス孝之
- 戦略相談: KURODO（Claude Project）

---

**作成日:** 2026年2月11日  
**作成者:** KURODO（Claude Sonnet 4）  
**バージョン:** 1.0  
**次回更新予定:** 機能追加時・ディレクトリ構造変更時


### docs/RENDER_DEPLOY_GUIDE.md

# Render デプロイガイド

暗号通貨監視ボットをRenderで自動実行する方法を説明します。

## 概要

このプロジェクトは、12の暗号通貨アカウントを1時間に1回監視し、新規ツイートをAI（Claude Sonnet 4）でリライトしてDiscordに通知します。

## デプロイ手順

### 1. GitHubリポジトリの準備

```bash
cd /Users/apple/Projects/x-auto-bot
git init
git add .
git commit -m "Initial commit: Crypto monitoring bot"
git remote add origin https://github.com/YOUR_USERNAME/x-auto-bot.git
git push -u origin main
```

### 2. Renderアカウント作成

1. [Render](https://render.com) にアクセス
2. GitHubアカウントで登録
3. リポジトリへのアクセスを許可

### 3. Cron Jobの作成

1. Renderダッシュボードで **New +** → **Cron Job** を選択
2. GitHubリポジトリを接続
3. 以下の設定を入力:

| 設定項目 | 値 |
|---------|---|
| **Name** | `crypto-monitor-bot` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python3 crypto_bot/cron_monitor_bot.py` |
| **Schedule** | `0 * * * *` (毎時0分に実行) |

### 4. 環境変数の設定

Renderの環境変数設定画面で以下を追加:

```plaintext
# Discord通知用
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_URL

# Anthropic API（Claude）
ANTHROPIC_API_KEY=sk-ant-YOUR_API_KEY

# X API（Developer アカウント - 読み取り用）
X_CONSUMER_KEY=YOUR_CONSUMER_KEY
X_CONSUMER_SECRET=YOUR_CONSUMER_SECRET
DEVELOPER_ACCESS_TOKEN=YOUR_DEVELOPER_ACCESS_TOKEN
DEVELOPER_ACCESS_TOKEN_SECRET=YOUR_DEVELOPER_ACCESS_TOKEN_SECRET

# X API（Bot アカウント - 投稿用）※現在は未使用
BOT_B_ACCESS_TOKEN=YOUR_BOT_ACCESS_TOKEN
BOT_B_ACCESS_SECRET=YOUR_BOT_ACCESS_SECRET
```

### 5. デプロイ実行

1. **Create Cron Job** をクリック
2. 初回デプロイが開始されます
3. ログで動作確認

## スケジュール設定

デフォルトは毎時0分に実行されます。変更する場合:

| スケジュール | Cron式 | 説明 |
|------------|--------|------|
| 毎時0分 | `0 * * * *` | デフォルト |
| 30分おき | `0,30 * * * *` | 毎時0分と30分 |
| 毎時15分 | `15 * * * *` | 毎時15分 |

## ログ確認

Renderダッシュボードの **Logs** タブで以下を確認できます:

- 監視対象アカウントの取得状況
- 新規ツイート検知
- AI生成ログ
- Discord通知送信結果

## トラブルシューティング

### ❌ API権限エラー (403 Forbidden)

**症状**: `⚠️  API権限制限 - 従量課金の有効化を待機中`

**原因**: X APIの従量課金がまだアクティブ化されていない

**解決策**:
1. X Developer Portal でクレジット購入済みか確認
2. 24-48時間待機（自動的にアクティブ化される）
3. または、X APIで投稿を行い、クレジットを消費してアクティブ化

### ⚠️  Discord通知が届かない

**確認事項**:
- `DISCORD_WEBHOOK_URL` が正しく設定されているか
- Discord Webhookが削除されていないか

### ⚠️  Claude生成エラー

**確認事項**:
- `ANTHROPIC_API_KEY` が正しく設定されているか
- Anthropic APIのクレジットが残っているか

## コスト

### Render

- **Free Plan**: Cron Jobは無料（月間750時間まで）
- 毎時実行でも月間費用は **$0**

### X API

- **従量課金**: 読み取り $0.005/リクエスト
- 12アカウント × 24回/日 = **$1.44/月** (最大)

### Anthropic API

- **Claude Sonnet 4**: $3.00 / 1M input tokens, $15.00 / 1M output tokens
- 月間推定コスト: **$5-10** (ツイート数による)

## 停止方法

1. Renderダッシュボードで該当のCron Jobを選択
2. **Settings** → **Delete Cron Job**

## 関連ファイル

- `/crypto_bot/cron_monitor_bot.py` - Cron Job用スクリプト
- `/render.yaml` - Render設定ファイル
- `/requirements.txt` - Python依存関係
- `/data/processed_tweets.txt` - 処理済みツイートID

### crypto_bot/QUICKSTART.md

# 暗号通貨監視ボット - クイックスタートガイド

## 🎯 このボットができること

指定された **12の暗号通貨アカウント** を1時間に1回自動監視し、新しい投稿があれば：

1. **Claude Sonnet 4** でリライト（元の核心 + あなたの意見）
2. **引用リポスト** として自動投稿
3. **重複投稿を防止**（SQLiteで管理）

## 📋 監視対象アカウント

1. @coinlikecoin
2. @taka__crypto
3. @yousukeakaban
4. @grvt_io
5. @etherealdex
6. @01exchange
7. @variational_io
8. @pacifica_fi
9. @basedonex
10. @miracletrade
11. @usetria
12. @hyperliquidx

## 🚀 1分でスタート

### ステップ1: 手動で動作確認

```bash
cd /Users/apple/Projects/x-auto-bot
python3 crypto_bot/auto_monitoring_bot.py
```

**期待される出力**:
- ✅ 新規投稿なし → 正常（対象アカウントが1時間以内に投稿していない）
- ✅ X件のツイートを取得 → リライト & 投稿が実行される

### ステップ2: 定期実行を設定（macOS）

```bash
cd /Users/apple/Projects/x-auto-bot/crypto_bot
./setup_scheduler.sh
```

これだけで **1時間ごとに自動実行** されます！

## 📊 ログの確認

```bash
# ボットのログをリアルタイム表示
tail -f /Users/apple/Projects/x-auto-bot/logs/auto_monitoring_bot.log
```

## ⚙️ カスタマイズ

### 監視対象アカウントを変更

`auto_monitoring_bot.py` の以下の部分を編集:

```python
TARGET_ACCOUNTS = [
    "coinlikecoin",
    "taka__crypto",
    # ... 追加・削除・変更可能
]
```

### AIの性格を変更

`auto_monitoring_bot.py` の `SYSTEM_PROMPT` を編集:

```python
SYSTEM_PROMPT = (
    "あなたは○○です。..."  # ← ここを変更
)
```

### 監視間隔を変更

**コード内**（`auto_monitoring_bot.py`）:
```python
MONITORING_INTERVAL_HOURS = 1  # ← 時間単位で変更
```

**launchd設定**（`com.user.crypto_monitoring_bot.plist`）:
```xml
<key>StartInterval</key>
<integer>3600</integer>  <!-- 秒単位（3600秒 = 1時間） -->
```

変更後は再設定が必要:
```bash
./setup_scheduler.sh
```

## 🛠 トラブルシューティング

### 「ModuleNotFoundError」が出る

```bash
pip3 install -r requirements.txt
```

### 「新規投稿なし」が続く

- 正常です（監視対象が1時間以内に投稿していない）
- 監視対象を増やす、または監視間隔を延ばす（例: 3時間前まで）

### 「投稿権限エラー」が出る

`.env` ファイルの以下を確認:

```env
X_CONSUMER_KEY=...
X_CONSUMER_SECRET=...
X_ACCESS_TOKEN=...        # Bot用アカウントのトークン
X_ACCESS_TOKEN_SECRET=... # Bot用アカウントのシークレット
```

### 定期実行が動かない

```bash
# 状態確認
launchctl list | grep crypto_monitoring_bot

# 再起動
launchctl stop com.user.crypto_monitoring_bot
launchctl start com.user.crypto_monitoring_bot

# ログ確認
tail -f /Users/apple/Projects/x-auto-bot/logs/monitoring_bot_stderr.log
```

## 🔄 定期実行の管理

### 停止

```bash
launchctl stop com.user.crypto_monitoring_bot
```

### 再開

```bash
launchctl start com.user.crypto_monitoring_bot
```

### 完全削除

```bash
launchctl unload ~/Library/LaunchAgents/com.user.crypto_monitoring_bot.plist
rm ~/Library/LaunchAgents/com.user.crypto_monitoring_bot.plist
```

## 💡 Tips

### 処理済みツイートをリセット

```bash
rm /Users/apple/Projects/x-auto-bot/data/processed_tweets.db
```

### 処理済みツイートを確認

```bash
sqlite3 /Users/apple/Projects/x-auto-bot/data/processed_tweets.db \
  "SELECT * FROM processed_tweets ORDER BY processed_at DESC LIMIT 10;"
```

### API使用量を確認

- Basicプラン: 月1万Read
- 1時間ごと実行: 月約720 Read（全く問題なし）
- OR検索を使用: 12アカウントを1リクエストで取得

## 📚 詳細ドキュメント

- [README_monitoring.md](./README_monitoring.md) - 詳細な使い方
- [auto_monitoring_bot.py](./auto_monitoring_bot.py) - ソースコード

## ❓ よくある質問

**Q: 何件くらい投稿されますか？**
A: 監視対象の投稿頻度次第ですが、1時間で0〜数件程度です。

**Q: 元ツイートは削除されませんか？**
A: されません。引用リポスト形式なので、元ツイートも表示されます。

**Q: スパムと見なされませんか？**
A: 引用リポスト + AI生成で独自性があるため、問題ありません。ただし、過度な頻度は避けましょう。

**Q: 複数のBotアカウントで実行できますか？**
A: `.env` の `BOT_B_ACCESS_TOKEN` などを使えば可能です。コードを少し修正する必要があります。


### crypto_bot/README_monitoring.md

# 暗号通貨監視ボット - 使い方

## 概要

指定された12の暗号通貨アカウントを1時間に1回監視し、Claude Sonnet 4でリライトして引用リポストするボットです。

## 監視対象アカウント（12名）

1. @coinlikecoin
2. @taka__crypto
3. @yousukeakaban
4. @grvt_io
5. @etherealdex
6. @01exchange
7. @variational_io
8. @pacifica_fi
9. @basedonex
10. @miracletrade
11. @usetria
12. @hyperliquidx

## 特徴

### API節約設計（Basicプラン対応）

- **OR検索で一括取得**: 1リクエストで全12アカウントの投稿を取得
- **時間指定検索**: 直近1時間の投稿のみを取得
- **重複チェック**: SQLiteで処理済みツイートを記録

### AI生成（Claude Sonnet 4）

- 元ツイートの核心を維持しつつ、表現を改善
- 独自の相場観・意見を1文追加
- 断定的な口調で140文字以内

## 実行方法

### 手動実行

```bash
cd /Users/apple/Projects/x-auto-bot
python3 crypto_bot/auto_monitoring_bot.py
```

### 定期実行（1時間ごと）

#### macOS（launchd）

1. **plistファイルを作成**:

```bash
# 以下の内容で ~/Library/LaunchAgents/com.user.crypto_monitoring_bot.plist を作成
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.crypto_monitoring_bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/python3</string>
        <string>/Users/apple/Projects/x-auto-bot/crypto_bot/auto_monitoring_bot.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/apple/Projects/x-auto-bot/logs/monitoring_bot_stdout.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/apple/Projects/x-auto-bot/logs/monitoring_bot_stderr.log</string>
</dict>
</plist>
```

2. **登録 & 起動**:

```bash
launchctl load ~/Library/LaunchAgents/com.user.crypto_monitoring_bot.plist
launchctl start com.user.crypto_monitoring_bot
```

3. **確認**:

```bash
launchctl list | grep crypto_monitoring_bot
```

4. **停止 & 削除**:

```bash
launchctl stop com.user.crypto_monitoring_bot
launchctl unload ~/Library/LaunchAgents/com.user.crypto_monitoring_bot.plist
```

#### Linux/Server（cron）

```bash
# crontabを編集
crontab -e

# 毎時0分に実行
0 * * * * cd /Users/apple/Projects/x-auto-bot && /usr/bin/python3 crypto_bot/auto_monitoring_bot.py >> logs/cron.log 2>&1
```

## ログ確認

```bash
# ボットのログ
tail -f /Users/apple/Projects/x-auto-bot/logs/auto_monitoring_bot.log

# launchd の標準出力/エラー
tail -f /Users/apple/Projects/x-auto-bot/logs/monitoring_bot_stdout.log
tail -f /Users/apple/Projects/x-auto-bot/logs/monitoring_bot_stderr.log
```

## データベース

処理済みツイートは以下のSQLiteデータベースに記録されます:

```
/Users/apple/Projects/x-auto-bot/data/processed_tweets.db
```

### データベース確認

```bash
sqlite3 /Users/apple/Projects/x-auto-bot/data/processed_tweets.db "SELECT * FROM processed_tweets ORDER BY processed_at DESC LIMIT 10;"
```

### データベースリセット（処理をやり直したい場合）

```bash
rm /Users/apple/Projects/x-auto-bot/data/processed_tweets.db
```

## トラブルシューティング

### 「新規投稿なし」が続く場合

- 監視対象アカウントが1時間以内に投稿していない可能性があります
- 検索クエリを確認: ログに `検索クエリ:` として出力されます

### API制限エラー

- Basicプランは月1万Readまで
- 1時間ごとの実行で月720回（30日）= 約720 Read（十分に余裕あり）

### 投稿権限エラー

- `.env` ファイルの `X_ACCESS_TOKEN` と `X_ACCESS_TOKEN_SECRET` が正しいか確認
- Bot用アカウントのトークンが設定されているか確認

## 設定のカスタマイズ

`auto_monitoring_bot.py` 内の定数を変更することで、動作をカスタマイズできます:

```python
# 監視間隔（時間）
MONITORING_INTERVAL_HOURS = 1

# 一度に取得する最大ツイート数
MAX_RESULTS = 100

# Claude System Prompt（AI の性格・口調を変更）
SYSTEM_PROMPT = "..."
```

## 注意事項

- **引用リポスト**: 元ツイートを引用する形で投稿されます
- **スパム対策**: 同じツイートは2度処理されません（SQLiteで管理）
- **レート制限**: `wait_on_rate_limit=True` により、制限時は自動で待機します


### crypto_bot/README_quote_tweet.md

# ツイートリライト & 引用リポストツール

## 🎯 機能

指定したツイートのURLまたはIDを入力すると、**Claude Sonnet 4** が暗号通貨有識者のペルソナでリライトし、引用リポストします。

## 🤖 AIのペルソナ

> **あなたは暗号通貨の黎明期から活躍する有識者であり、SNS運用のプロです。**
> 
> 経済・金融の幅広い知識を持ち、元ポストの意図を汲みつつ、より魅力的な文章に再構成する能力があります。
> 
> 元ツイートの「伝えたい核心」は維持したまま、構成と表現を編集し、最後にあなたの鋭い相場観や意見を1文付け加えてください。断定的な口調（～だ、～である）で、140文字以内に収めてください。

## 🚀 使い方

### 基本的な使い方

```bash
cd /Users/apple/Projects/x-auto-bot
python3 crypto_bot/quote_tweet.py <ツイートURL>
```

### 例

#### URLで指定

```bash
python3 crypto_bot/quote_tweet.py https://twitter.com/coinlikecoin/status/1234567890
```

または

```bash
python3 crypto_bot/quote_tweet.py https://x.com/taka__crypto/status/9876543210
```

#### ツイートIDで指定

```bash
python3 crypto_bot/quote_tweet.py 1234567890
```

## 📋 処理の流れ

1. **ツイート取得**: 指定されたツイートの内容を取得
2. **リライト生成**: Claude Sonnet 4 で有識者風にリライト
3. **確認プロンプト**: リライト内容を表示して確認
4. **引用リポスト**: Bot アカウント（@crypto_0101010）で投稿

## 💡 実行例

```bash
$ python3 crypto_bot/quote_tweet.py https://twitter.com/coinlikecoin/status/1234567890

======================================================================
ツイートリライト & 引用リポストツール
======================================================================

2026-02-10 21:20:00 - INFO - ツイートID: 1234567890
2026-02-10 21:20:01 - INFO - ツイートを取得中: ID 1234567890

----------------------------------------------------------------------
投稿者: コインくん (@coinlikecoin)
元ツイート:
  ビットコインが過去最高値を更新しました！今が買い時かもしれません。
----------------------------------------------------------------------

2026-02-10 21:20:02 - INFO - Claude Sonnet 4 でリライト生成中...
2026-02-10 21:20:05 - INFO - 生成されたリライト（135文字）:
  BTCが史上最高値を突破。しかし過熱感は否めない。短期的には調整局面に入る可能性が高い。むしろ押し目を待つべきだ。焦って高値掴みするな。

----------------------------------------------------------------------
リライト結果:
  BTCが史上最高値を突破。しかし過熱感は否めない。短期的には調整局面に入る可能性が高い。むしろ押し目を待つべきだ。焦って高値掴みするな。
----------------------------------------------------------------------

この内容で引用リポストしますか？ [y/N]: y

2026-02-10 21:20:10 - INFO - 引用リポストを投稿中...
2026-02-10 21:20:11 - INFO - ✅ 引用リポスト成功!
2026-02-10 21:20:11 - INFO -   URL: https://twitter.com/i/web/status/9999999999

======================================================================
✅ 処理完了！
======================================================================
```

## ⚙️ カスタマイズ

### AIのペルソナを変更

`quote_tweet.py` の `SYSTEM_PROMPT` を編集:

```python
SYSTEM_PROMPT = (
    "あなたは○○です。..."  # ← ここを変更
)
```

### 文字数制限を変更

```python
# 140文字制限を変更
if len(rewritten_text) > 280:  # ← 280文字に変更
    rewritten_text = rewritten_text[:277] + "..."
```

## 🛠 トラブルシューティング

### 「ツイートが見つかりませんでした」

- URLまたはIDが正しいか確認
- ツイートが削除されていないか確認
- 非公開アカウントのツイートは取得できません

### 「投稿権限エラー」

`.env` ファイルの認証情報を確認:

```env
X_CONSUMER_KEY=...
X_CONSUMER_SECRET=...
X_ACCESS_TOKEN=...        # Bot用アカウントのトークン
X_ACCESS_TOKEN_SECRET=... # Bot用アカウントのシークレット
```

### 「重複投稿エラー」

同じツイートに対して既に引用リポスト済みの場合、Xが重複と判断することがあります。
リライト内容を少し変えるか、時間をおいて再実行してください。

## 📊 ログ確認

```bash
tail -f /Users/apple/Projects/x-auto-bot/logs/quote_tweet.log
```

## 🔄 複数のツイートを処理

シェルスクリプトを作成して一括処理:

```bash
#!/bin/bash
# batch_quote.sh

TWEETS=(
    "https://twitter.com/coinlikecoin/status/1234567890"
    "https://twitter.com/taka__crypto/status/9876543210"
    "https://twitter.com/yousukeakaban/status/1111111111"
)

for tweet_url in "${TWEETS[@]}"; do
    echo "処理中: $tweet_url"
    python3 crypto_bot/quote_tweet.py "$tweet_url"
    echo "待機中（60秒）..."
    sleep 60  # API制限対策
done
```

## 💎 Tips

### ツイートURLの取得方法

1. Xアプリまたはブラウザでツイートを開く
2. 「共有」→「ツイートへのリンクをコピー」
3. コピーしたURLを使用

### おすすめの使い方

- 朝: 暗号通貨関連の人気ツイートをチェック
- 昼: 気になるツイートのURLをメモ
- 夜: まとめて `quote_tweet.py` で引用リポスト

## ⚠️ 注意事項

- **API制限**: 短時間に大量投稿すると制限されます（1時間に10-20件程度が目安）
- **著作権**: 引用リポストは適切に行ってください
- **スパム対策**: 同じアカウントへの過度な引用は避けましょう


### web/README.md

# X OAuth 2.0 クライアント管理 Webアプリ

複数のXアカウントをWebインターフェースで管理し、アクセストークンとリフレッシュトークンをデータベースに保存します。

## 機能

- 「Xでログイン」ボタンでOAuth 2.0認証
- アクセストークン＆リフレッシュトークンをDBに保存
- 登録済みアカウントの一覧表示・削除
- 長期運用に対応（リフレッシュトークンでトークン更新可能）

## セットアップ

### 1. X Developer Portal での設定

1. https://developer.x.com/ にアクセス
2. アプリを選択 → 「Settings」→ 「User authentication settings」→ 「Edit」
3. 以下を設定：

| 設定項目 | 値 |
|----------|-----|
| OAuth 2.0 | **有効化** |
| Type of App | **Web App** |
| Callback URI | `http://127.0.0.1:5000/callback` |
| Website URL | `http://127.0.0.1:5000` |

4. 「Save」後、「OAuth 2.0 Client ID and Client Secret」から以下を取得：
   - **Client ID**
   - **Client Secret**

### 2. 環境設定

```bash
cd /Users/apple/Projects/x-auto-bot/web

# .envファイルを作成
cp .env.example .env

# .envを編集してClient IDとSecretを設定
open -e .env
```

### 3. ライブラリインストール

```bash
# 仮想環境を有効化（親ディレクトリのものを使用）
source ../venv/bin/activate

# ライブラリをインストール
pip install -r requirements.txt
```

### 4. サーバー起動

```bash
python app.py
```

### 5. ブラウザでアクセス

http://127.0.0.1:5000 を開いて「Xでログイン」をクリック

## ファイル構成

```
web/
├── app.py           # Flaskアプリ本体
├── models.py        # DBモデルと操作関数
├── requirements.txt # 必要なライブラリ
├── .env             # 環境変数（自分で作成）
├── .env.example     # .envのテンプレート
├── users.db         # SQLiteデータベース（自動生成）
└── README.md        # このファイル
```

## OAuth 2.0 スコープ

| スコープ | 説明 |
|----------|------|
| `tweet.read` | ツイートの読み取り |
| `tweet.write` | ツイートの投稿 |
| `users.read` | ユーザー情報の読み取り |
| `offline.access` | リフレッシュトークンの取得（長期運用に必須） |

## データベーススキーマ

| カラム | 型 | 説明 |
|--------|-----|------|
| id | Integer | 主キー |
| twitter_user_id | String | XのユーザーID（ユニーク） |
| username | String | ユーザー名 |
| access_token | String | アクセストークン |
| refresh_token | String | リフレッシュトークン |
| token_expires_at | DateTime | トークン有効期限 |
| created_at | DateTime | 作成日時 |
| updated_at | DateTime | 更新日時 |

## トークンの更新（リフレッシュ）

アクセストークンの有効期限は2時間です。`refresh_token`を使って自動更新するには：

```python
import tweepy

# リフレッシュトークンでアクセストークンを更新
new_token = tweepy.OAuth2UserHandler.refresh_token(
    refresh_token=user.refresh_token,
    client_id=X_CLIENT_ID,
    client_secret=X_CLIENT_SECRET
)
```

## PostgreSQLへの移行

`.env`の`DATABASE_URL`を変更するだけで移行可能：

```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

※ `psycopg2` または `psycopg2-binary` のインストールが必要


---
## 最近の変更 (git log)

```
7b4ab03 render.yaml整理: 未使用サービス削除（コードはGit残存）
176b63b テキスト不足ツイートのスキップ + Claude拒否応答フィルター追加
33ca330 quote_tweet_id優先 + URL埋め込みフォールバック方式に変更
0df5912 リライトプロンプト改善: 元投稿への敬意を明示
920b39c DB planをbasic-256mbに修正（Renderの実環境に合わせる）
517e676 Cron Jobプランをfree→starterに変更（Render仕様変更対応）
6e5f981 自動引用投稿ボット追加 & バグ修正
198d537 Fix Render deployment error: Add missing dependencies
6b7ac14 Add image upload feature with Cloudflare R2 support
d3e404a Add auto-post monitoring bot for @crypto_0101010
```
