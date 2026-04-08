# Rabbit Video KPI Database — Schema Context

AIアナリスト用のDBスキーマ説明ファイル。
このファイルをコンテキストとして読み込み、自然言語でSQLクエリを生成できます。

## データベース: kpi.db (SQLite)

---

## テーブル: posts

投稿マスタ。1行 = 1動画。

| カラム | 型 | 説明 |
|---|---|---|
| id | INTEGER | 主キー (自動採番) |
| platform | TEXT | 'tiktok' または 'instagram' |
| post_id | TEXT | プラットフォーム固有の投稿ID |
| posted_at | TEXT | 投稿日時 (YYYY-MM-DD HH:MM) |
| post_hour | INTEGER | 投稿時刻 0-23 ← 時間帯分析用 |
| store_name | TEXT | 紹介した店舗名 |
| area | TEXT | 'kyoto' / 'nara' / サブエリア (例: 'kyoto_gion') |
| format | TEXT | 動画フォーマット (下記参照) |
| caption | TEXT | キャプション・ハッシュタグ |

**format の値**:
- `eating_scene` — 食べているシーン中心
- `intro` — 店舗紹介・外観
- `tour` — 店内ツアー
- `ranking` — ランキング形式
- `english` — 訪日外国人向け英語コンテンツ

---

## テーブル: daily_post_metrics

投稿ごとの日次指標スナップショット。

| カラム | 型 | 説明 |
|---|---|---|
| id | INTEGER | 主キー |
| platform | TEXT | 'tiktok' / 'instagram' |
| post_id | TEXT | posts.post_id への参照 |
| recorded_date | TEXT | 計測日 (YYYY-MM-DD) |
| views | INTEGER | 再生数 |
| likes | INTEGER | いいね数 |
| comments | INTEGER | コメント数 |
| shares | INTEGER | シェア数 |
| saves | INTEGER | 保存数 |

---

## テーブル: daily_account_metrics

アカウント全体の日次指標。

| カラム | 型 | 説明 |
|---|---|---|
| id | INTEGER | 主キー |
| platform | TEXT | 'tiktok' / 'instagram' |
| recorded_date | TEXT | 計測日 (YYYY-MM-DD) |
| followers | INTEGER | フォロワー数 |
| following | INTEGER | フォロー数 |
| total_likes | INTEGER | 累積いいね数 (TikTok) |

---

## ビュー: post_latest_metrics

各投稿の最新指標を結合したビュー。ほとんどの分析はこのビューから始める。

| カラム | 説明 |
|---|---|
| platform / post_id | 識別子 |
| posted_at / post_hour | 投稿日時・時刻 |
| store_name / area / format | 投稿属性 |
| views / likes / comments / shares / saves | 最新指標 |
| like_rate | likes/views × 100 (%) |
| comment_rate | comments/views × 100 (%) |

---

## 代表的な分析クエリ例

### 今週最も伸びた動画TOP5
```sql
SELECT store_name, format, views, like_rate
FROM post_latest_metrics
WHERE posted_at >= date('now', '-7 days')
ORDER BY views DESC LIMIT 5;
```

### フォーマット別平均再生数
```sql
SELECT format, COUNT(*) as cnt, ROUND(AVG(views),0) as avg_views
FROM post_latest_metrics
GROUP BY format ORDER BY avg_views DESC;
```

### 投稿時間と再生数の相関
```sql
SELECT post_hour, COUNT(*) as cnt, ROUND(AVG(views),0) as avg_views
FROM post_latest_metrics
WHERE post_hour IS NOT NULL
GROUP BY post_hour ORDER BY post_hour;
```

### フォロワー増加が多かった週
```sql
SELECT platform, recorded_date,
       followers - LAG(followers) OVER (PARTITION BY platform ORDER BY recorded_date) as gain
FROM daily_account_metrics
ORDER BY gain DESC LIMIT 10;
```

### 店舗別パフォーマンス (京都のみ)
```sql
SELECT store_name, COUNT(*) as posts, ROUND(AVG(views),0) as avg_views
FROM post_latest_metrics
WHERE area LIKE 'kyoto%'
GROUP BY store_name ORDER BY avg_views DESC;
```
