from telegram import Update
from telegram.ext import ContextTypes
from services.sheets_service import append_expense, generate_expense_id, get_monthly_total, update_expense_cell
from models.expense import Expense
from config import ALLOWED_USER_IDS, CATEGORIES, BUSINESSES
from handlers.photo_handler import pending_expenses
import re
from datetime import datetime


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """テキストメッセージのハンドラー"""
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        return

    text = update.message.text.strip()

    # 修正フローのチェック（数字1-5で始まる場合）
    if text and text[0] in "12345" and user_id in pending_expenses:
        await handle_correction(update, context, text)
        return

    # "OK"で確定
    if text.upper() == "OK" and user_id in pending_expenses:
        expense, row_number = pending_expenses[user_id]
        update_expense_cell(row_number, 14, "confirmed")
        del pending_expenses[user_id]
        await update.message.reply_text("✅ 確定しました。")
        return

    # コマンドチェック
    if text.startswith("/"):
        return  # コマンドハンドラーに任せる

    # テキスト経費入力の試行
    # フォーマット例：「交通費 梅田→京都 560円 事業3」
    await parse_text_expense(update, text)


async def parse_text_expense(update: Update, text: str):
    """テキストから経費情報をパース"""
    user_id = update.effective_user.id

    # 金額を抽出（数字+円 or ¥+数字）
    amount_match = re.search(r"[¥￥]?([\d,]+)円?", text)
    if not amount_match:
        await update.message.reply_text(
            "💡 経費を入力する場合：\n"
            "例）交通費 梅田→京都 560円 事業3\n"
            "例）Amazon 消耗品 3,200円\n"
            "📸 または領収書の写真を送信"
        )
        return

    amount = int(amount_match.group(1).replace(",", ""))
    tax_amount = amount * 10 // 110  # 消費税10%逆算

    # 事業番号を抽出
    biz_match = re.search(r"事業([0-4])", text)
    business_number = biz_match.group(1) if biz_match else "0"

    # 科目をキーワードから推定
    category_code = "99"
    category_keywords = {
        "03": ["交通", "電車", "タクシー", "バス", "新幹線", "飛行機"],
        "04": ["飲食", "食事", "ランチ", "ディナー", "飲み"],
        "05": ["消耗品", "Amazon", "文具", "備品", "USB", "ケーブル"],
        "01": ["サーバー", "API", "ドメイン", "通信", "Render", "Vercel"],
        "02": ["広告", "Indeed", "プロモ"],
        "06": ["手数料", "振込"],
        "07": ["外注", "プログラマー", "営業代行"],
        "10": ["書籍", "本", "Kindle", "Udemy"],
    }

    for code, keywords in category_keywords.items():
        if any(kw in text for kw in keywords):
            category_code = code
            break

    # 店名/内容を抽出（金額と事業番号を除いた部分）
    store_name = text
    store_name = re.sub(r"[¥￥]?[\d,]+円?", "", store_name)
    store_name = re.sub(r"事業[0-4]", "", store_name)
    store_name = store_name.strip()

    expense_id = generate_expense_id()
    expense = Expense(
        expense_id=expense_id,
        date=datetime.now().strftime("%Y/%m/%d"),
        amount=amount,
        tax_amount=tax_amount,
        store_name=store_name,
        category_code=category_code,
        category_name=CATEGORIES.get(category_code, "雑費"),
        business_number=business_number,
        business_name=BUSINESSES.get(business_number, "全社"),
        registration_method="text",
    )

    row_number = append_expense(expense.to_sheet_row())
    pending_expenses[user_id] = (expense, row_number)

    monthly_total = get_monthly_total()
    await update.message.reply_text(expense.to_confirmation_message(monthly_total))


async def handle_correction(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str):
    """修正フロー：1:日付 2:金額 3:店名 4:科目 5:事業"""
    user_id = update.effective_user.id
    expense, row_number = pending_expenses[user_id]

    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        await update.message.reply_text("修正値を入力してください。例：2 5000")
        return

    field_num = parts[0]
    new_value = parts[1].strip()

    # フィールド番号 → (シート列番号, モデル属性名)
    col_map = {
        "1": (2, "date"),            # B列：日付
        "2": (3, "amount"),          # C列：金額
        "3": (5, "store_name"),      # E列：店名
        "4": (6, "category_code"),   # F列：科目コード
        "5": (8, "business_number"), # H列：事業番号
    }

    if field_num not in col_map:
        return

    col_index, field_name = col_map[field_num]

    if field_num == "2":
        new_value_int = int(new_value.replace(",", "").replace("円", "").replace("¥", ""))
        update_expense_cell(row_number, col_index, new_value_int)
        update_expense_cell(row_number, 4, new_value_int * 10 // 110)  # 消費税再計算
        expense.amount = new_value_int
        expense.tax_amount = new_value_int * 10 // 110
    elif field_num == "4":
        update_expense_cell(row_number, col_index, new_value)
        update_expense_cell(row_number, 7, CATEGORIES.get(new_value, "雑費"))
        expense.category_code = new_value
        expense.category_name = CATEGORIES.get(new_value, "雑費")
    elif field_num == "5":
        update_expense_cell(row_number, col_index, new_value)
        update_expense_cell(row_number, 9, BUSINESSES.get(new_value, "全社"))
        expense.business_number = new_value
        expense.business_name = BUSINESSES.get(new_value, "全社")
    else:
        update_expense_cell(row_number, col_index, new_value)
        setattr(expense, field_name, new_value)

    update_expense_cell(row_number, 14, "corrected")

    monthly_total = get_monthly_total()
    await update.message.reply_text(
        f"✏️ 修正完了\n" + expense.to_confirmation_message(monthly_total)
    )
