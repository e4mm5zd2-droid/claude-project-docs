#!/usr/bin/env python3
"""
weekly_report.py - Rabbit Video 週次KPIレポート生成
使い方: python weekly_report.py [--week YYYY-WNN] [--db PATH] [--out PATH]
例:    python weekly_report.py --week 2026-W15
出力:  reports/weekly_YYYY-WNN.md
"""

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_DB = Path(__file__).parent / "data" / "kpi.db"
REPORTS_DIR = Path(__file__).parent / "reports"


def get_conn(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn


def week_range(iso_week: str) -> tuple[str, str]:
    """'2026-W15' → ('2026-04-06', '2026-04-12')"""
    year, w = iso_week.split("-W")
    monday = datetime.strptime(f"{year}-W{int(w):02d}-1", "%G-W%V-%u")
    sunday = monday + timedelta(days=6)
    return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")


def fetch_account_summary(conn: sqlite3.Connection, start: str, end: str) -> dict:  # type: ignore[return]
    sql = """
    SELECT platform,
           MIN(CASE WHEN recorded_date = ? THEN followers END) AS followers_start,
           MAX(CASE WHEN recorded_date = ? THEN followers END) AS followers_end
    FROM daily_account_metrics
    WHERE recorded_date BETWEEN ? AND ?
    GROUP BY platform
    """
    rows = conn.execute(sql, [start, end, start, end]).fetchall()
    result = {}
    for r in rows:
        start_f = r["followers_start"] or 0
        end_f = r["followers_end"] or 0
        result[r["platform"]] = {
            "followers_start": start_f,
            "followers_end": end_f,
            "gain": end_f - start_f,
        }
    return result


def fetch_top_posts_week(conn: sqlite3.Connection, start: str, end: str) -> list:
    sql = """
    SELECT
        p.platform,
        p.store_name,
        p.area,
        p.format,
        p.posted_at,
        MAX(m.views)    AS views,
        MAX(m.likes)    AS likes,
        MAX(m.comments) AS comments,
        ROUND(CAST(MAX(m.likes) AS REAL) / NULLIF(MAX(m.views), 0) * 100, 2) AS like_rate
    FROM posts p
    JOIN daily_post_metrics m
        ON p.platform = m.platform AND p.post_id = m.post_id
    WHERE p.posted_at BETWEEN ? AND ?
    GROUP BY p.platform, p.post_id
    ORDER BY views DESC
    LIMIT 5
    """
    return conn.execute(sql, [start, end + " 23:59"]).fetchall()


def fetch_format_summary(conn: sqlite3.Connection, start: str, end: str) -> list:
    sql = """
    SELECT
        p.format,
        COUNT(DISTINCT p.post_id)  AS posts,
        ROUND(AVG(m.views), 0)     AS avg_views,
        MAX(m.views)               AS max_views
    FROM posts p
    JOIN daily_post_metrics m
        ON p.platform = m.platform AND p.post_id = m.post_id
    WHERE p.posted_at BETWEEN ? AND ?
    AND m.recorded_date = (
        SELECT MAX(m2.recorded_date) FROM daily_post_metrics m2
        WHERE m2.platform = p.platform AND m2.post_id = p.post_id
    )
    GROUP BY p.format
    ORDER BY avg_views DESC
    """
    return conn.execute(sql, [start, end + " 23:59"]).fetchall()


def build_report(
    week: str,
    start: str,
    end: str,
    account: dict,
    top_posts: list,
    fmt_summary: list,
) -> str:  # noqa
    lines = [
        f"# Rabbit Video 週次KPIレポート {week}",
        f"**対象期間**: {start} 〜 {end}",
        f"**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
        "## 1. フォロワー推移",
        "",
    ]

    if account:
        lines.append("| プラットフォーム | 週初 | 週末 | 増減 |")
        lines.append("|---|---:|---:|---:|")
        for platform, d in account.items():
            sign = "+" if d["gain"] >= 0 else ""
            lines.append(
                f"| {platform} | {d['followers_start']:,} | {d['followers_end']:,} | {sign}{d['gain']:,} |"
            )
    else:
        lines.append("_(データなし)_")

    lines += [
        "",
        "---",
        "",
        "## 2. 週間TOP5動画",
        "",
    ]

    if top_posts:
        lines.append("| # | 店舗 | エリア | フォーマット | 再生数 | いいね率 |")
        lines.append("|---|---|---|---|---:|---:|")
        for i, r in enumerate(top_posts, 1):
            lines.append(
                f"| {i} | {r['store_name'] or '-'} | {r['area'] or '-'} | "
                f"{r['format'] or '-'} | {(r['views'] or 0):,} | {r['like_rate'] or 0}% |"
            )
    else:
        lines.append("_(データなし)_")

    lines += [
        "",
        "---",
        "",
        "## 3. フォーマット別パフォーマンス",
        "",
    ]

    if fmt_summary:
        lines.append("| フォーマット | 投稿数 | 平均再生数 | 最高再生数 |")
        lines.append("|---|---:|---:|---:|")
        for r in fmt_summary:
            lines.append(
                f"| {r['format'] or '未設定'} | {r['posts']} | "
                f"{int(r['avg_views'] or 0):,} | {int(r['max_views'] or 0):,} |"
            )
    else:
        lines.append("_(データなし)_")

    lines += [
        "",
        "---",
        "",
        "## 4. 次週アクション (AIアナリスト提案欄)",
        "",
        "- [ ] (analyze.py by_format の結果をもとに記入)",
        "- [ ] (analyze.py by_hour の結果をもとに記入)",
        "- [ ] (analyze.py by_store の結果をもとに記入)",
        "",
    ]

    return "\n".join(lines)


def current_iso_week() -> str:
    now = datetime.now()
    return f"{now.year}-W{now.isocalendar()[1]:02d}"


def main() -> None:
    parser = argparse.ArgumentParser(description="週次KPIレポートを生成する")
    parser.add_argument("--week", default=current_iso_week(), help="対象週 YYYY-WNN")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite DBパス")
    parser.add_argument("--out", help="出力ファイルパス (省略時は reports/weekly_WEEK.md)")
    args = parser.parse_args()

    start, end = week_range(args.week)
    conn = get_conn(Path(args.db))

    try:
        account = fetch_account_summary(conn, start, end)
        top = fetch_top_posts_week(conn, start, end)
        fmt = fetch_format_summary(conn, start, end)
    finally:
        conn.close()

    report = build_report(args.week, start, end, account, top, fmt)

    out_path = Path(args.out) if args.out else REPORTS_DIR / f"weekly_{args.week}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"✅ レポート生成完了: {out_path}")
    print(report)


if __name__ == "__main__":
    main()
