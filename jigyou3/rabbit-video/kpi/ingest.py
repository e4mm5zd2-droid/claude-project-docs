#!/usr/bin/env python3
"""
ingest.py - Rabbit Video KPI 日次データ取り込み
使い方:
  CSVから取り込み:  python ingest.py --csv posts.csv --type post_metrics
  アカウント指標:   python ingest.py --csv account.csv --type account_metrics
  新規投稿登録:     python ingest.py --csv new_posts.csv --type posts

CSVフォーマット:
  post_metrics:    platform,post_id,recorded_date,views,likes,comments,shares,saves
  account_metrics: platform,recorded_date,followers,following,total_likes
  posts:           platform,post_id,posted_at,store_name,area,format,caption
"""

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path(__file__).parent / "data" / "kpi.db"

REQUIRED_COLUMNS = {
    "post_metrics": {"platform", "post_id", "recorded_date", "views"},
    "account_metrics": {"platform", "recorded_date", "followers"},
    "posts": {"platform", "post_id"},
}


def get_conn(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        print(f"❌ DBが見つかりません: {db_path}")
        print("先に init_db.py を実行してください。")
        sys.exit(1)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def ingest_post_metrics(conn: sqlite3.Connection, rows: list) -> int:
    sql = """
    INSERT INTO daily_post_metrics
        (platform, post_id, recorded_date, views, likes, comments, shares, saves)
    VALUES
        (:platform, :post_id, :recorded_date,
         :views, :likes, :comments, :shares, :saves)
    ON CONFLICT(platform, post_id, recorded_date) DO UPDATE SET
        views    = excluded.views,
        likes    = excluded.likes,
        comments = excluded.comments,
        shares   = excluded.shares,
        saves    = excluded.saves
    """
    records = [
        {
            "platform": r["platform"],
            "post_id": r["post_id"],
            "recorded_date": r["recorded_date"],
            "views": int(r.get("views", 0) or 0),
            "likes": int(r.get("likes", 0) or 0),
            "comments": int(r.get("comments", 0) or 0),
            "shares": int(r.get("shares", 0) or 0),
            "saves": int(r.get("saves", 0) or 0),
        }
        for r in rows
    ]
    conn.executemany(sql, records)
    conn.commit()
    return len(records)


def ingest_account_metrics(conn: sqlite3.Connection, rows: list) -> int:
    sql = """
    INSERT INTO daily_account_metrics
        (platform, recorded_date, followers, following, total_likes)
    VALUES
        (:platform, :recorded_date, :followers, :following, :total_likes)
    ON CONFLICT(platform, recorded_date) DO UPDATE SET
        followers   = excluded.followers,
        following   = excluded.following,
        total_likes = excluded.total_likes
    """
    records = [
        {
            "platform": r["platform"],
            "recorded_date": r["recorded_date"],
            "followers": int(r.get("followers", 0) or 0),
            "following": int(r.get("following", 0) or 0),
            "total_likes": int(r.get("total_likes", 0) or 0),
        }
        for r in rows
    ]
    conn.executemany(sql, records)
    conn.commit()
    return len(records)


def ingest_posts(conn: sqlite3.Connection, rows: list) -> int:
    sql = """
    INSERT INTO posts
        (platform, post_id, posted_at, post_hour, store_name, area, format, caption)
    VALUES
        (:platform, :post_id, :posted_at, :post_hour, :store_name, :area, :format, :caption)
    ON CONFLICT(platform, post_id) DO UPDATE SET
        posted_at  = excluded.posted_at,
        post_hour  = excluded.post_hour,
        store_name = excluded.store_name,
        area       = excluded.area,
        format     = excluded.format,
        caption    = excluded.caption
    """
    records = []
    for r in rows:
        posted_at = r.get("posted_at", "")
        # posted_at が "YYYY-MM-DD HH:MM" 形式なら時刻を抽出
        post_hour = None
        if posted_at and len(posted_at) >= 13:
            try:
                post_hour = int(posted_at[11:13])
            except ValueError:
                pass
        records.append({
            "platform": r["platform"],
            "post_id": r["post_id"],
            "posted_at": posted_at,
            "post_hour": post_hour,
            "store_name": r.get("store_name", ""),
            "area": r.get("area", ""),
            "format": r.get("format", ""),
            "caption": r.get("caption", ""),
        })
    conn.executemany(sql, records)
    conn.commit()
    return len(records)


def load_csv(csv_path: Path) -> list:
    with open(csv_path, encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows


def validate_columns(rows: list[dict], ingest_type: str) -> None:
    if not rows:
        print("⚠️  CSVが空です")
        sys.exit(0)
    required = REQUIRED_COLUMNS.get(ingest_type, set())
    actual = set(rows[0].keys())
    missing = required - actual
    if missing:
        print(f"❌ 必須カラムが不足しています: {missing}")
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="KPI CSVをDBに取り込む")
    parser.add_argument("--csv", required=True, help="CSVファイルパス")
    parser.add_argument(
        "--type",
        required=True,
        choices=["post_metrics", "account_metrics", "posts"],
        help="取り込みデータ種別",
    )
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite DBパス")
    args = parser.parse_args()

    rows = load_csv(Path(args.csv))
    validate_columns(rows, args.type)

    conn = get_conn(Path(args.db))
    try:
        if args.type == "post_metrics":
            n = ingest_post_metrics(conn, rows)
        elif args.type == "account_metrics":
            n = ingest_account_metrics(conn, rows)
        else:
            n = ingest_posts(conn, rows)
        print(f"✅ {n}件 取り込み完了 (type={args.type})")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
