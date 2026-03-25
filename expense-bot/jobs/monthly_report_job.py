import asyncio
from datetime import datetime, timedelta
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, ALLOWED_USER_IDS
from services.report_service import generate_monthly_report_md
from services.github_service import commit_monthly_report


async def run():
    last = datetime.now().replace(day=1) - timedelta(days=1)
    ym_s = last.strftime("%Y/%m")
    ym_d = last.strftime("%Y-%m")
    md, tg = generate_monthly_report_md(ym_s)
    if not md:
        return
    ok = commit_monthly_report(ym_d, md)
    st = "✅ GitHub保存済" if ok else "⚠️ 保存失敗"
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    for uid in ALLOWED_USER_IDS:
        await bot.send_message(chat_id=uid, text=f"{tg}\n\n{st}")


if __name__ == "__main__":
    asyncio.run(run())
