"""
tests/test_kpi.py - Rabbit Video KPI システムのユニットテスト
実行: python -m pytest tests/ -v  (kpi/ ディレクトリ内から)
"""

import sqlite3
import sys
import tempfile
import csv
from datetime import datetime
from pathlib import Path

import pytest

# パスを通す
sys.path.insert(0, str(Path(__file__).parent.parent))

from init_db import init_db
from ingest import ingest_post_metrics, ingest_account_metrics, ingest_posts
from analyze import top_posts, by_format, by_hour, by_store, follower_growth
from weekly_report import week_range, build_report


# ---------- フィクスチャ ----------

@pytest.fixture
def db(tmp_path):
    """テスト用インメモリDBを初期化する"""
    db_path = tmp_path / "test_kpi.db"
    conn = init_db(db_path)
    yield conn
    conn.close()


@pytest.fixture
def seeded_db(db):
    """サンプルデータを投入したDB"""
    posts = [
        {
            "platform": "tiktok",
            "post_id": "TT001",
            "posted_at": "2026-04-01 19:00",
            "store_name": "錦市場 田中漬物",
            "area": "kyoto_nishiki",
            "format": "eating_scene",
            "caption": "#京都グルメ",
        },
        {
            "platform": "tiktok",
            "post_id": "TT002",
            "posted_at": "2026-04-02 12:00",
            "store_name": "嵐山よしむら",
            "area": "kyoto_arashiyama",
            "format": "intro",
            "caption": "#嵐山",
        },
        {
            "platform": "instagram",
            "post_id": "IG001",
            "posted_at": "2026-04-01 18:00",
            "store_name": "錦市場 田中漬物",
            "area": "kyoto_nishiki",
            "format": "eating_scene",
            "caption": "#Kyotofood",
        },
    ]
    ingest_posts(db, posts)

    metrics = [
        {
            "platform": "tiktok",
            "post_id": "TT001",
            "recorded_date": "2026-04-07",
            "views": 15200,
            "likes": 1320,
            "comments": 45,
            "shares": 210,
            "saves": 380,
        },
        {
            "platform": "tiktok",
            "post_id": "TT002",
            "recorded_date": "2026-04-07",
            "views": 8400,
            "likes": 520,
            "comments": 18,
            "shares": 95,
            "saves": 140,
        },
        {
            "platform": "instagram",
            "post_id": "IG001",
            "recorded_date": "2026-04-07",
            "views": 3200,
            "likes": 280,
            "comments": 22,
            "shares": 40,
            "saves": 190,
        },
    ]
    ingest_post_metrics(db, metrics)

    account_data = [
        {"platform": "tiktok", "recorded_date": "2026-04-01", "followers": 120, "following": 45, "total_likes": 2100},
        {"platform": "tiktok", "recorded_date": "2026-04-07", "followers": 210, "following": 48, "total_likes": 4950},
        {"platform": "instagram", "recorded_date": "2026-04-01", "followers": 85, "following": 60, "total_likes": 420},
        {"platform": "instagram", "recorded_date": "2026-04-07", "followers": 125, "following": 63, "total_likes": 680},
    ]
    ingest_account_metrics(db, account_data)

    return db


# ---------- init_db テスト ----------

class TestInitDb:
    def test_tables_created(self, db):
        tables = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
        assert "posts" in tables
        assert "daily_post_metrics" in tables
        assert "daily_account_metrics" in tables

    def test_view_created(self, db):
        views = {r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='view'").fetchall()}
        assert "post_latest_metrics" in views

    def test_idempotent(self, tmp_path):
        """2回初期化しても壊れないこと"""
        db_path = tmp_path / "idempotent.db"
        conn1 = init_db(db_path)
        conn1.close()
        conn2 = init_db(db_path)
        conn2.close()


# ---------- ingest テスト ----------

class TestIngestPosts:
    def test_insert(self, db):
        rows = [{"platform": "tiktok", "post_id": "P1", "posted_at": "2026-04-01 20:00",
                 "store_name": "テスト店", "area": "kyoto", "format": "eating_scene", "caption": ""}]
        n = ingest_posts(db, rows)
        assert n == 1
        count = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        assert count == 1

    def test_post_hour_extracted(self, db):
        rows = [{"platform": "tiktok", "post_id": "P2", "posted_at": "2026-04-01 19:30",
                 "store_name": "店A", "area": "nara", "format": "intro", "caption": ""}]
        ingest_posts(db, rows)
        hour = db.execute("SELECT post_hour FROM posts WHERE post_id='P2'").fetchone()[0]
        assert hour == 19

    def test_upsert(self, db):
        rows = [{"platform": "tiktok", "post_id": "P3", "posted_at": "2026-04-01 10:00",
                 "store_name": "旧店名", "area": "kyoto", "format": "intro", "caption": ""}]
        ingest_posts(db, rows)
        rows[0]["store_name"] = "新店名"
        ingest_posts(db, rows)
        name = db.execute("SELECT store_name FROM posts WHERE post_id='P3'").fetchone()[0]
        assert name == "新店名"
        count = db.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        assert count == 1


class TestIngestPostMetrics:
    def test_insert(self, seeded_db):
        count = seeded_db.execute("SELECT COUNT(*) FROM daily_post_metrics").fetchone()[0]
        assert count == 3

    def test_upsert_updates_views(self, seeded_db):
        updated = [{
            "platform": "tiktok", "post_id": "TT001",
            "recorded_date": "2026-04-07", "views": 99999,
            "likes": 1320, "comments": 45, "shares": 210, "saves": 380,
        }]
        ingest_post_metrics(seeded_db, updated)
        views = seeded_db.execute(
            "SELECT views FROM daily_post_metrics WHERE post_id='TT001' AND recorded_date='2026-04-07'"
        ).fetchone()[0]
        assert views == 99999
        count = seeded_db.execute("SELECT COUNT(*) FROM daily_post_metrics").fetchone()[0]
        assert count == 3  # 増えないこと

    def test_null_safe_conversion(self, seeded_db):
        rows = [{"platform": "tiktok", "post_id": "TT001",
                 "recorded_date": "2026-04-08", "views": "",
                 "likes": None, "comments": "", "shares": 0, "saves": ""}]
        ingest_post_metrics(seeded_db, rows)
        r = seeded_db.execute(
            "SELECT views, likes FROM daily_post_metrics WHERE post_id='TT001' AND recorded_date='2026-04-08'"
        ).fetchone()
        assert r[0] == 0
        assert r[1] == 0


class TestIngestAccountMetrics:
    def test_insert(self, seeded_db):
        count = seeded_db.execute("SELECT COUNT(*) FROM daily_account_metrics").fetchone()[0]
        assert count == 4  # 2プラットフォーム × 2日

    def test_upsert(self, seeded_db):
        updated = [{"platform": "tiktok", "recorded_date": "2026-04-07",
                    "followers": 300, "following": 50, "total_likes": 9999}]
        ingest_account_metrics(seeded_db, updated)
        followers = seeded_db.execute(
            "SELECT followers FROM daily_account_metrics WHERE platform='tiktok' AND recorded_date='2026-04-07'"
        ).fetchone()[0]
        assert followers == 300


# ---------- analyze テスト ----------

class TestAnalyze:
    def test_top_posts_returns_rows(self, seeded_db):
        rows = top_posts(seeded_db, None, 30)
        assert len(rows) > 0
        assert rows[0]["views"] >= rows[-1]["views"]  # 降順

    def test_top_posts_platform_filter(self, seeded_db):
        rows = top_posts(seeded_db, "instagram", 30)
        assert all(r["platform"] == "instagram" for r in rows)

    def test_by_format_groups(self, seeded_db):
        rows = by_format(seeded_db, 30)
        formats = {r["format"] for r in rows}
        assert "eating_scene" in formats
        assert "intro" in formats

    def test_by_hour_returns_hours(self, seeded_db):
        rows = by_hour(seeded_db, 30)
        hours = [r["post_hour"] for r in rows]
        assert 19 in hours  # TT001 は19時投稿

    def test_by_store_groups(self, seeded_db):
        rows = by_store(seeded_db, 30)
        stores = {r["store_name"] for r in rows}
        assert "錦市場 田中漬物" in stores

    def test_follower_growth_returns_rows(self, seeded_db):
        rows = follower_growth(seeded_db, 30)
        assert len(rows) > 0

    def test_empty_db_returns_empty(self, db):
        """データなしでもクラッシュしないこと"""
        assert top_posts(db, None, 30) == []
        assert by_format(db, 30) == []
        assert by_hour(db, 30) == []
        assert by_store(db, 30) == []
        assert follower_growth(db, 30) == []


# ---------- weekly_report テスト ----------

class TestWeeklyReport:
    def test_week_range(self):
        start, end = week_range("2026-W15")
        assert start == "2026-04-06"
        assert end == "2026-04-12"

    def test_week_range_w01(self):
        start, end = week_range("2026-W01")
        s = datetime.strptime(start, "%Y-%m-%d")
        e = datetime.strptime(end, "%Y-%m-%d")
        assert (e - s).days == 6
        assert s.weekday() == 0  # 月曜日

    def test_build_report_contains_header(self):
        report = build_report("2026-W15", "2026-04-06", "2026-04-12", {}, [], [])
        assert "Rabbit Video 週次KPIレポート 2026-W15" in report
        assert "2026-04-06" in report
        assert "2026-04-12" in report

    def test_build_report_with_data(self):
        account = {"tiktok": {"followers_start": 100, "followers_end": 200, "gain": 100}}
        report = build_report("2026-W15", "2026-04-06", "2026-04-12", account, [], [])
        assert "tiktok" in report
        assert "+100" in report

    def test_weekly_report_no_crash_on_empty(self, db, tmp_path):
        """空DBでもレポート生成がクラッシュしないこと"""
        from weekly_report import fetch_account_summary, fetch_top_posts_week, fetch_format_summary
        account = fetch_account_summary(db, "2026-04-06", "2026-04-12")
        top = fetch_top_posts_week(db, "2026-04-06", "2026-04-12")
        fmt = fetch_format_summary(db, "2026-04-06", "2026-04-12")
        report = build_report("2026-W15", "2026-04-06", "2026-04-12", account, top, fmt)
        assert "Rabbit Video" in report


# ---------- CSV サンプルファイルの整合性テスト ----------

class TestSampleFiles:
    SAMPLE_DIR = Path(__file__).parent.parent / "sample_data"

    def _read_csv(self, filename):
        path = self.SAMPLE_DIR / filename
        with open(path, encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))

    def test_posts_sample_columns(self):
        rows = self._read_csv("posts_sample.csv")
        required = {"platform", "post_id", "posted_at", "store_name", "area", "format"}
        assert required <= set(rows[0].keys())

    def test_post_metrics_sample_columns(self):
        rows = self._read_csv("post_metrics_sample.csv")
        required = {"platform", "post_id", "recorded_date", "views", "likes"}
        assert required <= set(rows[0].keys())

    def test_account_metrics_sample_columns(self):
        rows = self._read_csv("account_metrics_sample.csv")
        required = {"platform", "recorded_date", "followers"}
        assert required <= set(rows[0].keys())

    def test_sample_data_ingest_roundtrip(self, tmp_path):
        """サンプルCSVをDBに投入→読み出しが一致すること"""
        db_path = tmp_path / "roundtrip.db"
        conn = init_db(db_path)

        posts = self._read_csv("posts_sample.csv")
        metrics = self._read_csv("post_metrics_sample.csv")
        account = self._read_csv("account_metrics_sample.csv")

        ingest_posts(conn, posts)
        ingest_post_metrics(conn, metrics)
        ingest_account_metrics(conn, account)

        count = conn.execute("SELECT COUNT(*) FROM posts").fetchone()[0]
        assert count == len(posts)

        count = conn.execute("SELECT COUNT(*) FROM daily_post_metrics").fetchone()[0]
        assert count == len(metrics)

        rows = top_posts(conn, "tiktok", 365)
        assert len(rows) > 0

        conn.close()
