#!/usr/bin/env python3
"""
analyze.py - Rabbit Video KPI 分析クエリ集
使い方:
  python analyze.py top_posts [--platform tiktok] [--days 7]
  python analyze.py by_format [--days 30]
  python analyze.py by_hour [--days 30]
  python analyze.py by_store [--days 30]
  python analyze.py follower_growth [--days 30]
  python analyze.py weekly_report [--week YYYY-WNN]
"""

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

DEFAULT_DB = Path(__file__).parent / "data" / "kpi.db"


def get_conn(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


# ---------- クエリ関数 ----------

def top_posts(conn: sqlite3.Connection, platform: Optional[str], days: int) -> list:
    """再生数上位投稿を取得する"""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    params: list = [since]
    platform_clause = ""
    if platform:
        platform_clause = "AND p.platform = ?"
        params.append(platform)
    sql = f"""
    SELECT
        p.platform,
        p.post_id,
        p.posted_at,
        p.store_name,
        p.area,
        p.format,
        m.views,
        m.likes,
        m.comments,
        m.shares,
        ROUND(CAST(m.likes AS REAL) / NULLIF(m.views, 0) * 100, 2) AS like_rate
    FROM posts p
    JOIN daily_post_metrics m
        ON p.platform = m.platform AND p.post_id = m.post_id
    WHERE m.recorded_date = (
        SELECT MAX(m2.recorded_date)
        FROM daily_post_metrics m2
        WHERE m2.platform = p.platform AND m2.post_id = p.post_id
    )
    AND (p.posted_at >= ? OR p.posted_at IS NULL OR p.posted_at = '')
    {platform_clause}
    ORDER BY m.views DESC
    LIMIT 10
    """
    return conn.execute(sql, params).fetchall()


def by_format(conn: sqlite3.Connection, days: int) -> list:
    """フォーマット別平均再生数を集計する"""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    sql = """
    SELECT
        p.format,
        COUNT(DISTINCT p.post_id) AS post_count,
        ROUND(AVG(m.views), 0) AS avg_views,
        ROUND(AVG(CAST(m.likes AS REAL) / NULLIF(m.views, 0) * 100), 2) AS avg_like_rate
    FROM posts p
    JOIN daily_post_metrics m
        ON p.platform = m.platform AND p.post_id = m.post_id
    WHERE m.recorded_date = (
        SELECT MAX(m2.recorded_date)
        FROM daily_post_metrics m2
        WHERE m2.platform = p.platform AND m2.post_id = p.post_id
    )
    AND (p.posted_at >= ? OR p.posted_at IS NULL OR p.posted_at = '')
    GROUP BY p.format
    ORDER BY avg_views DESC
    """
    return conn.execute(sql, [since]).fetchall()


def by_hour(conn: sqlite3.Connection, days: int) -> list:
    """投稿時間帯別平均再生数を集計する"""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    sql = """
    SELECT
        p.post_hour,
        COUNT(DISTINCT p.post_id) AS post_count,
        ROUND(AVG(m.views), 0) AS avg_views,
        ROUND(AVG(CAST(m.likes AS REAL) / NULLIF(m.views, 0) * 100), 2) AS avg_like_rate
    FROM posts p
    JOIN daily_post_metrics m
        ON p.platform = m.platform AND p.post_id = m.post_id
    WHERE p.post_hour IS NOT NULL
    AND m.recorded_date = (
        SELECT MAX(m2.recorded_date)
        FROM daily_post_metrics m2
        WHERE m2.platform = p.platform AND m2.post_id = p.post_id
    )
    AND (p.posted_at >= ? OR p.posted_at IS NULL OR p.posted_at = '')
    GROUP BY p.post_hour
    ORDER BY p.post_hour
    """
    return conn.execute(sql, [since]).fetchall()


def by_store(conn: sqlite3.Connection, days: int) -> list:
    """店舗別平均再生数を集計する"""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    sql = """
    SELECT
        p.store_name,
        p.area,
        COUNT(DISTINCT p.post_id) AS post_count,
        ROUND(AVG(m.views), 0) AS avg_views,
        MAX(m.views) AS max_views
    FROM posts p
    JOIN daily_post_metrics m
        ON p.platform = m.platform AND p.post_id = m.post_id
    WHERE p.store_name IS NOT NULL AND p.store_name != ''
    AND m.recorded_date = (
        SELECT MAX(m2.recorded_date)
        FROM daily_post_metrics m2
        WHERE m2.platform = p.platform AND m2.post_id = p.post_id
    )
    AND (p.posted_at >= ? OR p.posted_at IS NULL OR p.posted_at = '')
    GROUP BY p.store_name, p.area
    ORDER BY avg_views DESC
    LIMIT 20
    """
    return conn.execute(sql, [since]).fetchall()


def follower_growth(conn: sqlite3.Connection, days: int) -> list:
    """フォロワー推移を取得する"""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    sql = """
    SELECT
        platform,
        recorded_date,
        followers,
        followers - LAG(followers) OVER (PARTITION BY platform ORDER BY recorded_date) AS daily_gain
    FROM daily_account_metrics
    WHERE recorded_date >= ?
    ORDER BY platform, recorded_date
    """
    return conn.execute(sql, [since]).fetchall()


# ---------- フォーマッタ ----------

def print_table(rows: list[sqlite3.Row], title: str) -> None:
    if not rows:
        print(f"\n{title}\n(データなし)\n")
        return
    cols = rows[0].keys()
    widths = {c: max(len(str(c)), max(len(str(r[c] or "")) for r in rows)) for c in cols}
    header = "  ".join(str(c).ljust(widths[c]) for c in cols)
    sep = "  ".join("-" * widths[c] for c in cols)
    print(f"\n## {title}")
    print(header)
    print(sep)
    for r in rows:
        print("  ".join(str(r[c] or "").ljust(widths[c]) for c in cols))
    print()


# ---------- CLI ----------

def main() -> None:
    parser = argparse.ArgumentParser(description="KPI分析クエリを実行する")
    parser.add_argument(
        "query",
        choices=["top_posts", "by_format", "by_hour", "by_store", "follower_growth"],
        help="実行するクエリ",
    )
    parser.add_argument("--platform", choices=["tiktok", "instagram"], help="絞り込むプラットフォーム")
    parser.add_argument("--days", type=int, default=30, help="集計期間(日数) デフォルト30")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite DBパス")
    args = parser.parse_args()

    conn = get_conn(Path(args.db))
    try:
        if args.query == "top_posts":
            rows = top_posts(conn, args.platform, args.days)
            title = f"再生数TOP10 (過去{args.days}日)"
            if args.platform:
                title += f" [{args.platform}]"
            print_table(rows, title)

        elif args.query == "by_format":
            rows = by_format(conn, args.days)
            print_table(rows, f"フォーマット別パフォーマンス (過去{args.days}日)")

        elif args.query == "by_hour":
            rows = by_hour(conn, args.days)
            print_table(rows, f"投稿時間帯別パフォーマンス (過去{args.days}日)")

        elif args.query == "by_store":
            rows = by_store(conn, args.days)
            print_table(rows, f"店舗別パフォーマンス (過去{args.days}日)")

        elif args.query == "follower_growth":
            rows = follower_growth(conn, args.days)
            print_table(rows, f"フォロワー推移 (過去{args.days}日)")

    finally:
        conn.close()


if __name__ == "__main__":
    main()
