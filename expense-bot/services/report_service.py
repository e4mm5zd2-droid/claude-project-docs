from datetime import datetime, timedelta
from services.sheets_service import get_monthly_summary
from config import TOTAL_MONTHLY_BUDGET, MONTHLY_BUDGETS

BIZ_NAMES = {"0": "全社", "1": "アフィリ", "2": "Xツール", "3": "求人", "4": "CRM"}


def generate_monthly_report_md(year_month: str = None) -> tuple[str, str]:
    """(markdown_full, telegram_short)を返す"""
    if year_month is None:
        last = datetime.now().replace(day=1) - timedelta(days=1)
        year_month = last.strftime("%Y/%m")
    dm = year_month.replace("/", "-")
    s = get_monthly_summary(year_month)
    if s["total"] == 0:
        return "", "該当月のデータなし"

    total = s["total"]
    ratio = total / TOTAL_MONTHLY_BUDGET * 100 if TOTAL_MONTHLY_BUDGET > 0 else 0

    md = f"# 月次経費レポート {dm}\n\n"
    md += f"**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    md += f"## サマリー\n\n| 項目 | 金額 |\n|------|------|\n"
    md += f"| 合計 | ¥{total:,} |\n| 予算 | ¥{TOTAL_MONTHLY_BUDGET:,} |\n"
    md += f"| 消化率 | {ratio:.1f}% |\n| 残 | ¥{max(0, TOTAL_MONTHLY_BUDGET - total):,} |\n\n"

    md += f"## 事業別\n\n| 事業 | 金額 | 予算 | 消化率 |\n|------|------|------|--------|\n"
    for bn, amt in sorted(s.get("by_business_raw", {}).items()):
        b = MONTHLY_BUDGETS.get(bn, 0)
        r = (amt / b * 100) if b > 0 else 0
        md += f"| 事業{bn}:{BIZ_NAMES.get(bn, bn)} | ¥{amt:,} | ¥{b:,} | {r:.0f}% |\n"

    md += f"\n## 科目別\n\n| 科目 | 金額 | 構成比 |\n|------|------|--------|\n"
    for cat, amt in s["by_category"].items():
        md += f"| {cat} | ¥{amt:,} | {amt / total * 100:.1f}% |\n"
    md += f"\n---\n*自動生成 by KURODO Finance Bot*\n"

    tg = f"📊 月次レポート {dm}\n━━━━━━━━━━━━\n"
    tg += f"💰 合計:¥{total:,}(予算比{ratio:.0f}%)\n\n【事業別】\n"
    for bn, amt in sorted(s.get("by_business_raw", {}).items()):
        tg += f"  事業{bn}({BIZ_NAMES.get(bn, bn)}):¥{amt:,}\n"
    tg += f"\n詳細→finance/monthly_report/{dm}.md"
    return md, tg
