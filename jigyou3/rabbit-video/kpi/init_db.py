#!/usr/bin/env python3
"""
init_db.py - Rabbit Video KPI データベース初期化
使い方: python init_db.py [--db PATH]
"""

import argparse
import sqlite3
from pathlib import Path

DEFAULT_DB = Path(__file__).parent / "data" / "kpi.db"
SCHEMA_FILE = Path(__file__).parent / "schema.sql"


def init_db(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    schema = SCHEMA_FILE.read_text(encoding="utf-8")
    conn.executescript(schema)
    conn.commit()
    return conn


def main() -> None:
    parser = argparse.ArgumentParser(description="KPI DB を初期化する")
    parser.add_argument("--db", default=str(DEFAULT_DB), help="SQLite DBパス")
    args = parser.parse_args()

    db_path = Path(args.db)
    conn = init_db(db_path)
    conn.close()
    print(f"✅ DB初期化完了: {db_path}")


if __name__ == "__main__":
    main()
