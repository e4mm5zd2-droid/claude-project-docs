# yt-x-thread-bot - YouTube→X自動スレッド投稿ボット

> YouTube動画の字幕を取得し、Claude APIで要約、X（Twitter）にスレッド形式で自動投稿するボット

*最終更新: 2026-03-18*

**リポジトリ**: https://github.com/e4mm5zd2-droid/yt-x-thread-bot
**パス**: `/Users/apple/Projects/yt-x-thread-bot`

---

## アーキテクチャ（分離パイプライン）

YouTubeがクラウドIPをブロックするため、字幕取得と投稿を分離。

```
[GitHub Actions] 15分ごと
  → channels.json の監視チャンネルから新着動画を自動発見
  → webshare.io プロキシ（日本住宅IP）経由で字幕取得
  → PostgreSQL に status="transcript_ready" で保存

[Render Cron Job] 1時間ごと
  → DB から transcript_ready の動画を1件取得
  → Claude API で要約 → 2ツイートのスレッド生成
  → X API でリプライチェーン投稿
  → status="completed" に更新
```

## 投稿フォーマット

- 2ツイート構成のリプライチェーン（スレッド）
- 1ツイート目: 要点まとめ（280文字以内）、最後は「引き」で終わる
- 2ツイート目: リプライで結論を軽く触れる（140文字以内）
- YouTube URLは付けない
- ハッシュタグは2ツイート目の末尾に付与

## 手動操作

| やりたいこと | 方法 |
|-------------|------|
| すぐ字幕取得 | GitHub Actions → Fetch Transcripts → Run workflow |
| すぐ投稿 | Render ダッシュボード → yt-x-thread-bot → Trigger Run |
| チャンネル追加 | `channels.json` を編集して push |
| ローカルテスト | `python3 bot.py --url "URL" --dry-run` |
| ローカル投稿 | `python3 bot.py --url "URL"` |

## 主要リンク

- GitHub Actions: https://github.com/e4mm5zd2-droid/yt-x-thread-bot/actions
- GitHub Secrets: https://github.com/e4mm5zd2-droid/yt-x-thread-bot/settings/secrets/actions
- Render: https://dashboard.render.com/

## 環境変数

### GitHub Secrets
- `DATABASE_URL` — Render PostgreSQL の External URL
- `YOUTUBE_API_KEY` — YouTube Data API v3
- `PROXY_URL` — webshare.io Rotating Residential プロキシ（日本IP）

### Render 環境変数
- `DATABASE_URL` — 自動注入（fromDatabase）
- `X_CONSUMER_KEY/SECRET` — X API (x-video-bot App)
- `X_ACCESS_TOKEN/SECRET` — X API (@tabiga_daisukii)
- `X_BEARER_TOKEN` — X API
- `ANTHROPIC_API_KEY` — Claude API（要約生成）
- `OPENAI_API_KEY` — Whisper フォールバック用
- `YOUTUBE_API_KEY` — メタデータ取得用

## コマンド

```bash
# ドライラン（投稿しない）
python3 bot.py --url "https://youtu.be/xxxxx" --dry-run

# 実投稿
python3 bot.py --url "https://youtu.be/xxxxx"

# fetch モード（字幕取得のみ・GitHub Actions用）
python3 bot.py --mode fetch --limit 5

# post モード（要約＋投稿のみ・Render用）
python3 bot.py --mode post --limit 1
```

## 監視チャンネル

`channels.json` で管理。チャンネル追加は `channels.json` を編集して push するだけ。
- @sns_sakiyomi (SAKIYOMI)

## 技術スタック

- youtube-transcript-api — 字幕取得（プロキシ対応）
- yt-dlp — フォールバック
- Claude API (claude-sonnet-4-6) — 要約生成
- tweepy v2 — X投稿
- SQLAlchemy + PostgreSQL — DB
- GitHub Actions — 字幕取得cron
- Render — 投稿cron + DB

---

## ディレクトリ構成

```
├── .github/workflows/
│   └── fetch-transcripts.yml
├── db/
│   ├── connection.py
│   └── models.py
├── docs/
│   ├── ARCHITECTURE.md
│   └── RENDER_DEPLOY.md
├── monitor/
│   └── channel_watcher.py
├── poster/
│   └── x_poster.py
├── prompts/
│   ├── thread_ja.txt
│   ├── thread_en.txt
│   └── longform_ja.txt
├── scripts/
│   ├── gen_x_token.py
│   ├── healthcheck.py
│   ├── setup_channels.py
│   └── test_post.py
├── summarizer/
│   └── claude_summarizer.py
├── transcriber/
│   ├── subtitle_extractor.py
│   ├── text_cleaner.py
│   └── whisper_fallback.py
├── bot.py
├── channels.json
├── config.py
├── render.yaml
└── requirements.txt
```

---

## デプロイ設定 (render.yaml)

```yaml
databases:
  - name: yt-x-thread-bot-db
    plan: free

services:
  - type: cron
    name: yt-x-thread-bot
    runtime: python
    plan: starter
    schedule: "0 * * * *"
    startCommand: python3 bot.py --mode post --limit 1
```
