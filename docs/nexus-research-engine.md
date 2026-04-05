# NEXUS Research Engine (NRE)

## 概要
自由なクエリを入力すると、5つの情報ソースを横断検索し、AIスコアリングで精査した上で構造化されたリサーチレポートを返すシステム。Telegram Bot経由で操作し、投資・暗号通貨リサーチに活用。

## 技術スタック
| カテゴリ | 技術 |
|---|---|
| 言語 | Python 3.11 |
| フレームワーク | Pydantic v2, SQLAlchemy 2.0 |
| AI/LLM | Claude API（スコアリング・要約）, xAI Grok API（X検索） |
| DB | Supabase PostgreSQL + pgvector |
| ベクトル検索 | sentence-transformers (all-MiniLM-L6-v2) |
| Bot | python-telegram-bot v20+ |
| デプロイ | Mac mini常時稼働（手動起動） |

## アーキテクチャ
```
nexus-research-engine/
├── nre/
│   ├── main.py              # エントリポイント
│   ├── connectors/          # 5ソース検索コネクタ
│   │   ├── x_grok.py        # X/SNS (Grok API)
│   │   ├── web_ddg.py       # Web (DuckDuckGo)
│   │   ├── hackernews.py    # HackerNews
│   │   ├── rss.py           # RSSフィード
│   │   └── intelligence.py  # Intelligence DB
│   ├── scoring/             # AIスコアリング
│   ├── storage/             # DB・ベクトル保存
│   └── bot/                 # Telegram Bot
├── tests/
├── reports/                 # 生成レポート保存先
└── requirements.txt
```

## データフロー
```
ユーザー（Telegram）
  → /research <クエリ>
  → Query Analyzer (Claude API)
  → Search Orchestrator（5コネクタ並列実行）
  → Result Aggregator（重複排除）
  → Claude Scorer（関連性・信頼性・鮮度・アクション性の4軸評価）
  → Report Generator（Markdown形式）
  → DB保存 + ベクトル埋め込み
  → Telegram返信
```

## 起動方法
```bash
# Telegram Botモード（本番）
python -m nre.main

# CLIモード（開発テスト用）
python -m nre.main --cli --query "AI agent 最新動向"

# テスト
pytest tests/ -v
```

### 環境変数（キー名のみ）
- TELEGRAM_BOT_TOKEN
- TELEGRAM_ALLOWED_USERS
- ANTHROPIC_API_KEY
- XAI_API_KEY
- DATABASE_URL
- NRE_MAX_RESULTS_PER_SOURCE
- NRE_MIN_SCORE_THRESHOLD
- NRE_REPORT_DIR
- NRE_LOG_LEVEL

## 現在の状態
- [ ] 開発中 / [ ] 稼働中 / [x] 停止中

## 関連事業
事業1(アフィリ) / 統括
