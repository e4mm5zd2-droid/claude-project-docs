# On The Edge - サービス全体概要

*最終更新: 2026-02-28 19:21*

---
## 会社・ビジネス情報


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
| openai | smartnr (^6.21.0), smartnr (1.59.5) |
| psycopg2-binary | x-auto-bot (2.9.9), smartnr (2.9.11) |
| python-dotenv | x-auto-bot (?), smartnr (1.2.1) |
| react | corporate-site (^19.2.0), smartnr (19.2.3) |
| react-dom | corporate-site (^19.2.0), smartnr (19.2.3) |
