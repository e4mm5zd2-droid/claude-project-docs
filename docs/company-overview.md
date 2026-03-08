# On The Edge - サービス全体概要

*最終更新: 2026-03-08 14:01*

---
## 会社・ビジネス情報


### 20260308_新規録音.md

# ミーティングメモ: マーケティング戦略・新商品開発に関する打ち合わせ
*日時: 2026-03-08*
*音声ファイル: 新規録音.m4a*

## 要約
かおりちゃんの現在のビジネス構造（公式LINE・フロントセミナー・講座販売）を確認しながら、女性ターゲットに向けたマーケティング戦略を議論した。今後の主要プロモーションとして6〜7月以降の高額物販スクール（約100万円）が予定されており、それに向けたSNS運用・新商品開発の方向性を検討した。AIやLINEボット等を活用した新サービスの可能性についても意見交換を行い、次回までに提供可能な機能を整理して共有することになった。

---

## 議題

### 1. 現在のビジネス構造・マネタイズ方法
- 公式LINEはリスト収集目的で運用。イベント（フロントセミナー）開催時に活用
- フロントセミナーは無料開催し、そこで講座を販売するモデル
- 主な商材：
  - **手帳活用術講座**：ZOOMオンラインセミナー（後期4回 ＋ ワンワンセッション2回）、価格8万円弱
  - **ノウハウ系コンテンツ**：Note有料記事、メールコンテンツ等（低価格帯）
- 過去はビジネス講座メインだったが、受講者からの要望で恋愛系のコーチングも対応（都度クローズド対応）
- 集客チャネル：Facebookコミュニティ、Instagram、メタ広告（現状は活発でなく、今後強化予定）

### 2. ターゲット・SNS戦略
- **ターゲットは女性に絞っており、今後も男性への販売は考えていない**
- 女性向けにはXよりもNote・アメブロの方が響くと判断し、Xはこれまで積極活用してこなかった
- X・Threadsの自動投稿ツールについて議論：
  - 高インプレッション投稿を分析・抽出し、類似コンテンツをAIで量産する手法を紹介
  - プロフィールにInstagram・FacebookのURLを掲載し、各プラットフォームへ誘導する設計が有効
  - Xからnoteへの誘導も可能

### 3. 今後の大型プロモーション（物販スクール）
- 時期：6〜7月以降（4〜5月に打ち合わせ予定）
- 内容：輸入物販のノウハウ ＋ シングルマザーでも実現できるライフスタイルを掛け合わせたコース
- 形式：コラボ開催
- 価格：**約100万円**の高額商品

### 4. 新商品・新サービスのアイデア検討
- LINEボットを活用したQOL向上ツールの商品化について議論：
  - チャット形式でGoogleカレンダーへの自動登録など、日常タスクを自動化できる機能を提案
  - かおりちゃんから「めちゃくちゃいい」と高評価
- X・Threads向けの**長文コンテンツ自動運用講座**の販売可能性：
  - 1万〜3万円程度の価格帯で販売可能との見通し
  - かおりちゃん自身が内容を理解・消化できれば自分のコミュニティで販売できると合意
- 現在提供可能な機能が急速に増えているため、一度まとめて共有する必要あり

---

## 決定事項
- [x] 女性ターゲットのマーケティングに集中し、男性向け展開は当面行わない
- [x] X・Threads運用はかおりちゃん自身が行うかどうか保留とし、まず「X運用講座」としての商品化を検討する
- [x] 6〜7月以降に物販スクール（高額コラボ）のプロモーションを実施する

---

## 今後のアクション
- [ ] 提供可能な機能・サービスを箇条書きにまとめてLINEで送付（担当: 話者側・議事録作成者）
- [ ] 送付された内容を確認・返信し、新商品のアイデアを膨らませる（担当: かおりちゃん）
- [ ] メタ広告の運用を強化する方針を具体化する（担当: かおりちゃん）
- [ ] 4〜5月に物販スクールのコラボ打ち合わせを実施（担当: かおりちゃん）

---
## サービス一覧

| サービス | 概要 | 技術スタック | デプロイ |
|---------|------|------------|---------|
| X Auto Bot - 暗号通貨監視・自動投稿ボット | X (Twitter) 自動投稿ボット。Claude AIで暗号通貨ニュースを監視・要約し自動投稿 | tweepy, anthropic, Flask, SQLAlchemy | Render |
| On The Edge コーポレートサイト | 会社コーポレートサイト。React + Vite SPA、Framer Motion、Tailwin | framer-motion, react | Render |
| SmartNR - ナイトワーク スカウト管理アプリ | スカウト業務管理アプリ。Next.js フロントエンド + FastAPI バックエンド | next, react, fastapi, SQLAlchemy, supabase | Render |
| LINE Claude Bot | LINE Messaging API + Claude AI チャットボット。Google Maps | @line/bot-sdk, @anthropic-ai/sdk, express | ? (Docker) |

---
## Render デプロイ構成


### X Auto Bot - 暗号通貨監視・自動投稿ボット

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
  # 監視にxAI Grok APIを使用。X API Readクレジット消費ゼロ。
  - type: cron
    name: crypto-auto-quote-bot
    runtime: python
    plan: starter
    schedule: "0 */2 * * *"  # 2時間ごとに実行
    buildCommand: pip install -r requirements.txt
    startCommand: python3 crypto_bot/auto_quote_monitor.py --limit 4
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: XAI_API_KEY
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: X_CONSUMER_KEY
        sync: false
      - key: X_CONSUMER_SECRET
        sync: false
      - key: X_ACCESS_TOKEN
        sync: false
      - key: X_ACCESS_TOKEN_SECRET
        sync: false

  # SOU_BTC 監視(Grok x_search) → リライト(Claude) → 投稿(X API)
  # 監視にxAI Grok APIを使用。X API Readクレジット消費ゼロ。
  - type: cron
    name: sou-btc-inspire-cron
    runtime: python
    plan: starter
    schedule: "* * * * *"  # 毎分実行（リアルタイム監視）
    buildCommand: pip install -r requirements.txt
    startCommand: python3 crypto_bot/sou_btc_inspire_monitor.py --limit 1
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: XAI_API_KEY
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: X_CONSUMER_KEY
        sync: false
      - key: X_CONSUMER_SECRET
        sync: false
      - key: X_ACCESS_TOKEN
        sync: false
      - key: X_ACCESS_TOKEN_SECRET
        sync: false

  # Triaアフィリエイトボット（1時間ごと）
  # 海外CT速報(Grok x_search) → Claude翻訳+Tria訴求 → 引用リポスト → リプライでLinktreeリンク
  # X API Readクレジット消費ゼロ
  - type: cron
    name: affiliate-bot
    runtime: python
    plan: starter
    schedule: "30 * * * *"
    buildCommand: pip install -r requirements.txt
    startCommand: python3 crypto_bot/affiliate_bot.py
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: XAI_API_KEY
        sync: false
      - key: ANTHROPIC_API_KEY
        sync: false
      - key: LINKTREE_URL
        sync: false
      - key: X_CONSUMER_KEY
        sync: false
      - key: X_CONSUMER_SECRET
        sync: false
      - key: BOT_B_ACCESS_TOKEN
        sync: false
      - key: BOT_B_ACCESS_SECRET
        sync: false

  # SOU_BTC Filtered Stream（無効化済み）
  # - type: worker
  #   name: sou-btc-inspire-stream
  #   ...

```

### On The Edge コーポレートサイト

```yaml
services:
  - type: web
    name: on-the-edge-corporate-v2
    env: static
    buildCommand: npm install && npm run build
    staticPublishPath: ./dist
    routes:
      - type: rewrite
        source: /*
        destination: /index.html

```

### SmartNR - ナイトワーク スカウト管理アプリ

```yaml
services:
  # FastAPI バックエンド
  - type: web
    name: smartnr-backend
    runtime: python
    region: singapore
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        sync: false
      - key: SUPABASE_URL
        sync: false
      - key: SUPABASE_KEY
        sync: false
      - key: XAI_API_KEY
        sync: false
      - key: XAI_BASE_URL
        value: https://api.x.ai/v1
      - key: APP_NAME
        value: SmartNR API
      - key: DEBUG
        value: false
      - key: SECRET_KEY
        generateValue: true
      - key: ALLOWED_ORIGINS
        value: https://smartnr-frontend.onrender.com,https://smartnr.vercel.app

  # Next.js フロントエンド
  - type: web
    name: smartnr-frontend
    runtime: node
    region: singapore
    buildCommand: cd frontend && npm install && npm run build
    startCommand: cd frontend && npm start
    envVars:
      - key: NODE_VERSION
        value: 20.11.0
      - key: NEXT_PUBLIC_API_URL
        value: https://smartnr-backend.onrender.com
      - key: NEXT_PUBLIC_SUPABASE_URL
        sync: false
      - key: NEXT_PUBLIC_SUPABASE_ANON_KEY
        sync: false

```

---
## 技術スタック横断まとめ


### 複数プロジェクトで共通の依存関係

| パッケージ | 使用プロジェクト |
|-----------|----------------|
| SQLAlchemy | x-auto-bot (2.0.0), smartnr (2.0.46) |
| lucide-react | corporate-site (^0.575.0), smartnr (^0.563.0) |
| openai | x-auto-bot (1.0.0), smartnr (^6.21.0), smartnr (1.59.5) |
| psycopg2-binary | x-auto-bot (2.9.9), smartnr (2.9.11) |
| python-dotenv | x-auto-bot (?), smartnr (1.2.1) |
| react | corporate-site (^19.2.0), smartnr (19.2.3) |
| react-dom | corporate-site (^19.2.0), smartnr (19.2.3) |
