from telegram import Update
from telegram.ext import ContextTypes
from config import ALLOWED_USER_IDS
from services.report_service import generate_monthly_report_md


async def handle_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USER_IDS:
        return
    args = context.args
    ym = args[0] if args else None
    md, tg = generate_monthly_report_md(ym)
    if not md:
        await update.message.reply_text("📊 データなし")
        return
    await update.message.reply_text(tg)
    if args and len(args) > 1 and args[1] == "save":
        from services.github_service import commit_monthly_report
        ok = commit_monthly_report(ym.replace("/", "-"), md)
        await update.message.reply_text("✅ GitHub保存完了" if ok else "⚠️ 保存失敗")
