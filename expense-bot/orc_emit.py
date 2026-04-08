"""軽量イベント発行ヘルパー - 各サービスにコピーして使用

依存: requests のみ。失敗してもサービス側は止めない。
"""
from __future__ import annotations

import os
import requests

EVENT_SERVER_URL = os.getenv("ORC_EVENT_URL", "http://localhost:5100")
EVENT_SECRET = os.getenv("ORC_EVENT_SECRET", "kurodo_event_2026")


def emit_event(event_type, source, data, timeout=5):
    """ote-orchestratorイベントサーバーにイベントを送信"""
    try:
        resp = requests.post(
            f"{EVENT_SERVER_URL}/events",
            json={
                "event_type": event_type,
                "source": source,
                "data": data,
                "secret": EVENT_SECRET,
            },
            timeout=timeout,
        )
        return resp.json() if resp.status_code == 200 else None
    except Exception:
        return None
