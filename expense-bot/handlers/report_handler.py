from telegram import Update
from telegram.ext import ContextTypes
from services.sheets_service import get_monthly_summary
from config import ALLOWED_USER_IDS


async def handle_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """月次レポートコマンド /report [YYYY/MM]"""
    user_id = update.effective_user.id
    if user_id not in ALLOWED_USER_IDS:
        return

    # 引数から年月を取得（なければ今月）
    args = context.args
    year_month = args[0] if args else None

    summary = get_monthly_summary(year_month)

    if summary["total"] == 0:
        await update.message.reply_text("📊 該当月のデータがありません。")
        return

    # レポート生成
    report = f"📊 月次経費レポート\n━━━━━━━━━━━━━━\n💰 合計: ¥{summary['total']:,}\n\n"

    report += "【事業別】\n"
    for biz, amount in summary["by_business"].items():
        report += f"  {biz}: ¥{amount:,}\n"

    report += "\n【科目別TOP5】\n"
    for i, (cat, amount) in enumerate(summary["by_category"].items()):
        if i >= 5:
            break
        pct = amount / summary["total"] * 100
        report += f"  {cat}: ¥{amount:,} ({pct:.0f}%)\n"

    await update.message.reply_text(report)
