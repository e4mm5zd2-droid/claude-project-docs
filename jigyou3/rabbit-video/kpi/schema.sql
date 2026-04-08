-- Rabbit Video KPI Database Schema
-- 京都・奈良グルメアカウント パフォーマンス管理DB

-- 投稿マスタ: 1行 = 1動画
CREATE TABLE IF NOT EXISTS posts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    platform    TEXT    NOT NULL CHECK(platform IN ('tiktok', 'instagram')),
    post_id     TEXT    NOT NULL,           -- プラットフォーム固有ID
    posted_at   TEXT,                       -- 投稿日時 ISO8601 (YYYY-MM-DD HH:MM)
    post_hour   INTEGER,                    -- 投稿時刻(0-23) ← 相関分析用
    store_name  TEXT,                       -- 店舗名
    area        TEXT,                       -- 'kyoto' / 'nara' / サブエリア
    format      TEXT,                       -- 'eating_scene' / 'intro' / 'tour' / 'ranking'
    caption     TEXT,                       -- キャプション・タグ
    created_at  TEXT    DEFAULT (datetime('now')),
    UNIQUE(platform, post_id)
);

-- 日次投稿指標: 投稿ごとに毎日スナップショット
CREATE TABLE IF NOT EXISTS daily_post_metrics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    platform        TEXT    NOT NULL,
    post_id         TEXT    NOT NULL,
    recorded_date   TEXT    NOT NULL,       -- YYYY-MM-DD
    views           INTEGER DEFAULT 0,
    likes           INTEGER DEFAULT 0,
    comments        INTEGER DEFAULT 0,
    shares          INTEGER DEFAULT 0,
    saves           INTEGER DEFAULT 0,
    UNIQUE(platform, post_id, recorded_date),
    FOREIGN KEY(platform, post_id) REFERENCES posts(platform, post_id)
);

-- 日次アカウント指標: プラットフォームごとに毎日1行
CREATE TABLE IF NOT EXISTS daily_account_metrics (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    platform        TEXT    NOT NULL,
    recorded_date   TEXT    NOT NULL,       -- YYYY-MM-DD
    followers       INTEGER DEFAULT 0,
    following       INTEGER DEFAULT 0,
    total_likes     INTEGER DEFAULT 0,      -- 累積いいね(TikTok)
    UNIQUE(platform, recorded_date)
);

-- 分析ビュー: 投稿メタ + 最新指標
CREATE VIEW IF NOT EXISTS post_latest_metrics AS
SELECT
    p.platform,
    p.post_id,
    p.posted_at,
    p.post_hour,
    p.store_name,
    p.area,
    p.format,
    m.recorded_date AS latest_date,
    m.views,
    m.likes,
    m.comments,
    m.shares,
    m.saves,
    ROUND(CAST(m.likes AS REAL) / NULLIF(m.views, 0) * 100, 2) AS like_rate,
    ROUND(CAST(m.comments AS REAL) / NULLIF(m.views, 0) * 100, 2) AS comment_rate
FROM posts p
JOIN daily_post_metrics m
    ON p.platform = m.platform AND p.post_id = m.post_id
WHERE m.recorded_date = (
    SELECT MAX(m2.recorded_date)
    FROM daily_post_metrics m2
    WHERE m2.platform = p.platform AND m2.post_id = p.post_id
);
