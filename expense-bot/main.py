import logging
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters
from config import TELEGRAM_BOT_TOKEN
from handlers.photo_handler import handle_photo
from handlers.text_handler import handle_text
from handlers.report_handler import handle_report

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main():
    """ボット起動"""
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # ハンドラー登録
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CommandHandler("report", handle_report))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("経費ボット起動")
    app.run_polling(drop_pending_updates=True)


async def help_command(update, context):
    """ヘルプメッセージ"""
    await update.message.reply_text(
        "💰 経費管理ボット\n"
        "━━━━━━━━━━━━\n"
        "📸 領収書の写真を送信 → 自動登録\n"
        "✏️ テキスト入力 → 例：交通費 梅田→京都 560円 事業3\n"
        "📊 /report → 今月の経費サマリー\n"
        "📊 /report 2026/03 → 指定月のサマリー\n"
        "━━━━━━━━━━━━\n"
        "登録後の修正：\n"
        "  1 2026/03/24 → 日付修正\n"
        "  2 5000 → 金額修正\n"
        "  3 スタバ → 店名修正\n"
        "  4 04 → 科目修正\n"
        "  5 3 → 事業修正\n"
        "  OK → 確定"
    )


if __name__ == "__main__":
    main()
