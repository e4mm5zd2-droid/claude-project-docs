# X Video Bot - メディア自動転載ボット

> X (Twitter) 動画・メディアの自動転載ボット。yt-dlp + tweepy で動画取得→投稿

*最終更新: 2026-04-04 14:44*

**パス**: `/Users/apple/Projects/business2-x-tools/x-video-bot`
**ブランチ**: `master`

---
## README.md

# x-video-bot

指定アカウント（X / TikTok / YouTube / Instagram）から動画・画像を自動取得し、自分のXアカウントに転載するボット。

## 対応メディア

| ソース | 動画 | 画像 | 取得方法 |
|--------|------|------|----------|
| X | o | o | tweepy v2 API |
| TikTok | o | o | yt-dlp |
| YouTube Shorts | o | - | yt-dlp |
| Instagram | o | o | instaloader + yt-dlp |

## セットアップ

```bash
cd /Users/apple/Projects/business2-x-tools/x-video-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
brew install yt-dlp

cp .env.example .env
# .env に新規X Developer Accountのキーを記入
```

## 設定

### accounts.json
監視対象アカウントを設定:
```json
{
  "accounts": [
    {"platform": "x", "username": "example", "enabled": true},
    {"platform": "tiktok", "username": "example", "enabled": true},
    {"platform": "youtube", "channel_url": "https://www.youtube.com/@example", "enabled": true},
    {"platform": "instagram", "username": "example", "enabled": true}
  ]
}
```

### captions.txt
投稿時のキャプション（1行1キャプション、ランダム選択）。

### .env
- `X_API_KEY/SECRET`, `X_ACCESS_TOKEN/SECRET`, `X_BEARER_TOKEN` — 新規Developer Account
- `R2_*` — Cloudflare R2 設定
- `MAX_POSTS_PER_RUN` (default: 2), `MAX_POSTS_PER_DAY` (default: 24), `POST_INTERVAL` (default: 120秒), `FETCH_LIMIT` (default: 5)

### Render デプロイ
- 1時間2投稿・1日24投稿で運用
- 詳細: [docs/RENDER_DEPLOY.md](docs/RENDER_DEPLOY.md)

## 使い方

```bash
# 通常実行
python bot.py

# ドライラン（投稿せず確認のみ）
python bot.py --dry-run

# 件数制限
python bot.py --limit 1
```

## 検証

```bash
python -c "from config import *; print('Config OK')"
python -c "from fetcher import fetch_all_media; print('Fetcher OK')"
python -c "from poster import get_api_v1, get_client_v2; print('Poster OK')"
python -c "from storage import get_r2_client; print('Storage OK')"
python bot.py --dry-run --limit 1
```

## アーキテクチャ

```
accounts.json → fetcher.py → downloader.py → poster.py → storage.py
                                                ↑
                                            bot.py (orchestration)
```

- `fetcher.py` — X API v2 / yt-dlp / instaloader でメディアURL取得
- `downloader.py` — yt-dlp で動画DL / requests で画像DL
- `poster.py` — tweepy v1.1 media_upload + v2 create_tweet
- `storage.py` — boto3 で Cloudflare R2 にアップロード
- `bot.py` — 全体オーケストレーション


---
## 技術スタック


### Python Dependencies

```
tweepy
boto3
python-dotenv
requests
instaloader
yt-dlp
```

---
## ディレクトリ構成

```
├── docs/
│   └── RENDER_DEPLOY.md
├── media/
│   └── 81de51e6d71c.mp4
├── .env.example
├── .gitignore
├── README.md
├── accounts.json
├── bot.py
├── captions.txt
├── config.py
├── downloader.py
├── fetcher.py
├── posted_log.json
├── poster.py
├── render.yaml
├── requirements.txt
└── storage.py
```

---
## デプロイ設定 (render.yaml)

```yaml
# ===========================================
# x-video-bot - Render Cron Job
# ===========================================
# 1時間ごとに実行、1回あたり最大2投稿、1日24投稿まで

services:
  - type: cron
    name: x-video-bot
    runtime: python
    plan: starter
    schedule: "0 * * * *"  # 毎時0分に実行（1時間ごと）
    buildCommand: pip install -r requirements.txt
    startCommand: python3 bot.py
    envVars:
      - key: PYTHON_VERSION
        value: "3.11.0"
      - key: X_API_KEY
        sync: false
      - key: X_API_SECRET
        sync: false
      - key: X_ACCESS_TOKEN
        sync: false
      - key: X_ACCESS_TOKEN_SECRET
        sync: false
      - key: X_BEARER_TOKEN
        sync: false
      - key: R2_ENDPOINT_URL
        sync: false
      - key: R2_ACCESS_KEY_ID
        sync: false
      - key: R2_SECRET_ACCESS_KEY
        sync: false
      - key: R2_BUCKET_NAME
        sync: false
      - key: MAX_POSTS_PER_RUN
        value: "2"
      - key: MAX_POSTS_PER_DAY
        value: "24"
      - key: POST_INTERVAL
        value: "120"
      - key: FETCH_LIMIT
        value: "5"

```

---
## 最近の変更 (git log)

```
c559624 fix: POST_INTERVAL を 120 秒に修正（Render Cron 向け）
7e8d485 Instagram 一時無効化（429 レート制限対策）
31178f9 1時間2投稿・1日24投稿に変更、Renderデプロイ対応（render.yaml, R2永続化）
7c6f17c feat: Instagram 対応追加 (instaloader + yt-dlp)
0f106a8 init: x-video-bot — X/TikTok/YouTube メディア自動転載ボット
```
