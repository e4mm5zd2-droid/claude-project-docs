# LINE Claude Bot

> LINE Messaging API + Claude AI チャットボット。Google Maps・Web検索連携

*最終更新: 2026-02-28 19:21*

**パス**: `/Users/apple/Projects/shared/line-claude-bot`
**ブランチ**: `main`

---
## README.md

# LINE Claude Bot

LINE Messaging API + Claude AI + Google Maps API + Tavily Search API を統合したチャットボット

## 機能

- **Claude AI 対話**: Claude Sonnet 4.5 による自然な日本語対話
- **Google Maps 統合**: 
  - 場所検索（「梅田近くのカフェ」）
  - ルート案内（距離・時間・手順）
  - ジオコーディング（住所→座標）
- **Tavily Web検索**: 最新ニュース・情報検索
- **Claude Tool Use**: AI が自律的に適切なツールを選択

## 必要なAPIキー（5つ）

| APIキー | 取得元 | 無料枠 |
|--------|--------|--------|
| LINE_CHANNEL_ACCESS_TOKEN | [LINE Developers Console](https://developers.line.biz/) | 無料 |
| LINE_CHANNEL_SECRET | LINE Developers Console | 無料 |
| ANTHROPIC_API_KEY | [console.anthropic.com](https://console.anthropic.com/) | 従量課金 |
| GOOGLE_MAPS_API_KEY | [Google Cloud Console](https://console.cloud.google.com/) | 月$200無料 |
| TAVILY_API_KEY | [app.tavily.com](https://app.tavily.com/) | 月1,000回無料 |

## デプロイ手順

### 1. GitHub リポジトリ作成

```bash
git init
git add .
git commit -m "Initial commit: LINE Claude Bot"
git remote add origin https://github.com/YOUR_USERNAME/line-claude-bot.git
git push -u origin main
```

### 2. Render デプロイ

1. [Render Dashboard](https://dashboard.render.com/) → **New +** → **Web Service**
2. GitHub リポジトリを接続
3. 設定:
   - **Environment**: Docker
   - **Plan**: Free
   - **Health Check Path**: `/health`
4. **Environment** タブで5つの環境変数を設定
5. **Deploy latest commit** をクリック

### 3. LINE Webhook URL 設定

LINE Developers Console → Messaging API 設定:

1. **Webhook URL**: `https://your-app.onrender.com/webhook`
2. **Webhookの利用**: 有効化
3. **応答メッセージ**: 無効化（重要）
4. **Webhook URL を検証** で疎通確認

## 動作確認

### ヘルスチェック
```bash
curl https://your-app.onrender.com/health
```

### LINE でテスト
- 「こんにちは」→ 通常会話
- 「大阪駅から鶴野町への行き方」→ ルート案内 + Google Maps URL
- 「渋谷駅近くのカフェ」→ 場所検索 + 各店舗の Maps URL
- 「今日のAIニュース」→ Tavily Web検索結果

## コスト見積もり

| サービス | 無料枠 | 想定 |
|---------|--------|------|
| Render | 月750時間 | 無料 |
| LINE | 無料 | 無料 |
| Claude Sonnet 4.5 | 入力$3/MTok, 出力$15/MTok | 月数百円〜 |
| Google Maps | 月$200 | 無料枠内 |
| Tavily | 月1,000回 | 無料枠内 |

## トラブルシューティング

| 症状 | 対処 |
|------|------|
| 既読のみで返信なし | Renderログ確認 |
| ツールが使われない | `tools` パラメータ確認 |
| Google Maps URLが出ない | システムプロンプト確認 |
| 二重返信される | LINE Console で「応答メッセージ」を無効化 |

## 拡張案

- 画像付き返信（Google Maps Static API）
- 位置情報連携（LINEの位置情報メッセージ）
- リッチメニュー
- 音声認識（Whisper API）
- 画像認識（Claude Vision）


---
## 技術スタック

### Dependencies

| Package | Version |
|---------|---------|
| @anthropic-ai/sdk | ^0.39.0 |
| @googlemaps/google-maps-services-js | ^3.4.0 |
| @line/bot-sdk | ^9.7.0 |
| @tavily/core | ^0.7.1 |
| express | ^4.21.2 |

### Scripts

```json
{
  "start": "node index.js"
}
```

---
## ディレクトリ構成

```
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── index.js
└── package.json
```

---
## 最近の変更 (git log)

```
c671b41 feat: Add detailed error logging for Directions API
2cfc183 Initial commit: LINE Claude Bot with Maps & Search
```
