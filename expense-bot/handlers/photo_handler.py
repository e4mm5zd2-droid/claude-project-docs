from telegram import Update
from telegram.ext import ContextTypes
from services.ocr_service import analyze_receipt
from services.sheets_service import append_expense, generate_expense_id, get_monthly_total
from models.expense import Expense
from config import ALLOWED_USER_IDS, CATEGORIES, BUSINESSES

# ユーザーごとの最新経費を保持（修正フロー用）
pending_expenses: dict[int, tuple[Expense, int]] = {}  # user_id -> (expense, row_number)


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """写真受信時のハンドラー"""
    user_id = update.effective_user.id

    # アクセス制限
    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("⛔ アクセス権限がありません。")
        return

    await update.message.reply_text("📸 解析中...")

    # 最大サイズの写真を取得
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    image_bytes = await file.download_as_bytearray()

    # Claude Vision APIで解析
    result = await analyze_receipt(bytes(image_bytes))

    # Expenseオブジェクト作成
    expense_id = generate_expense_id()
    expense = Expense(
        expense_id=expense_id,
        date=result.get("date", ""),
        amount=result.get("amount", 0),
        tax_amount=result.get("tax_amount", 0),
        store_name=result.get("store_name", ""),
        category_code=result.get("category_code", "99"),
        category_name=CATEGORIES.get(result.get("category_code", "99"), "雑費"),
        business_number=result.get("business_number", "0"),
        business_name=BUSINESSES.get(result.get("business_number", "0"), "全社"),
        memo=result.get("memo", ""),
        registration_method="photo",
        image_file_id=photo.file_id,
    )

    # Google Sheetsに登録
    row_number = append_expense(expense.to_sheet_row())

    # 修正用に保持
    pending_expenses[user_id] = (expense, row_number)

    # 今月累計を取得
    monthly_total = get_monthly_total()

    # 確認メッセージを送信
    await update.message.reply_text(expense.to_confirmation_message(monthly_total))
