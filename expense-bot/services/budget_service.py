from services.sheets_service import get_monthly_summary

# ote-orchestrator イベント発行
try:
    from orc_emit import emit_event as _orc_emit
except ImportError:
    _orc_emit = None
from config import MONTHLY_BUDGETS, TOTAL_MONTHLY_BUDGET, ALERT_THRESHOLD, BUDGET_ALERT_ENABLED

BIZ_NAMES = {"0": "全社", "1": "アフィリ", "2": "Xツール", "3": "求人", "4": "CRM"}


def check_budget() -> dict:
    if not BUDGET_ALERT_ENABLED:
        return {"total": 0, "budget": TOTAL_MONTHLY_BUDGET, "ratio": 0, "remaining": TOTAL_MONTHLY_BUDGET, "alerts": []}
    summary = get_monthly_summary()
    total = summary["total"]
    alerts = []
    ratio = total / TOTAL_MONTHLY_BUDGET if TOTAL_MONTHLY_BUDGET > 0 else 0

    if ratio >= 1.0:
        alerts.append(f"🚨 月間予算超過！¥{total:,}/¥{TOTAL_MONTHLY_BUDGET:,}({ratio:.0%})")
    elif ratio >= ALERT_THRESHOLD:
        alerts.append(f"⚠️ 月間予算{ratio:.0%}到達 ¥{total:,}/¥{TOTAL_MONTHLY_BUDGET:,}")

    for biz_num, amt in summary.get("by_business_raw", {}).items():
        budget = MONTHLY_BUDGETS.get(biz_num, 0)
        if budget <= 0:
            continue
        r = amt / budget
        name = BIZ_NAMES.get(biz_num, biz_num)
        if r >= 1.0:
            alerts.append(f"🚨 事業{biz_num}({name})超過 ¥{amt:,}/¥{budget:,}")
        elif r >= ALERT_THRESHOLD:
            alerts.append(f"⚠️ 事業{biz_num}({name}){r:.0%} ¥{amt:,}/¥{budget:,}")

    # ote-orchestrator にアラートイベント発行
    if _orc_emit and alerts:
        _orc_emit("expense.threshold", "expense-bot", {
            "total_expense": total,
            "budget": TOTAL_MONTHLY_BUDGET,
            "burn_rate": ratio,
            "alerts": alerts,
        })

    return {
        "total": total,
        "budget": TOTAL_MONTHLY_BUDGET,
        "ratio": ratio,
        "remaining": max(0, TOTAL_MONTHLY_BUDGET - total),
        "alerts": alerts,
    }
