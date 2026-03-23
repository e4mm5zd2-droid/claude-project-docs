import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import GOOGLE_SHEETS_ID, GOOGLE_SERVICE_ACCOUNT_JSON

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

credentials = Credentials.from_service_account_file(
    GOOGLE_SERVICE_ACCOUNT_JSON, scopes=SCOPES
)
gc = gspread.authorize(credentials)
spreadsheet = gc.open_by_key(GOOGLE_SHEETS_ID)


def get_expense_sheet():
    """経費台帳シートを取得（なければ作成）"""
    try:
        return spreadsheet.worksheet("経費台帳")
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title="経費台帳", rows=1000, cols=14)
        headers = [
            "ID", "日付", "金額(税込)", "消費税額", "店名/支払先",
            "科目コード", "勘定科目", "事業番号", "事業名",
            "備考", "登録方法", "画像ID", "登録日時", "ステータス",
        ]
        ws.append_row(headers)
        return ws


def generate_expense_id() -> str:
    """経費IDを生成（EXP-YYYYMMDD-NNN）"""
    today = datetime.now().strftime("%Y%m%d")
    ws = get_expense_sheet()
    all_values = ws.get_all_values()

    today_count = sum(1 for row in all_values[1:] if row[0].startswith(f"EXP-{today}"))
    return f"EXP-{today}-{today_count + 1:03d}"


def append_expense(row: list) -> int:
    """経費台帳に1行追加。追加した行番号を返す"""
    ws = get_expense_sheet()
    ws.append_row(row, value_input_option="USER_ENTERED")
    return len(ws.get_all_values())


def update_expense_cell(row_number: int, col_index: int, value):
    """特定セルを更新（修正フロー用）"""
    ws = get_expense_sheet()
    ws.update_cell(row_number, col_index, value)


def get_monthly_total(year_month: str = None) -> int:
    """今月の経費合計を取得"""
    if year_month is None:
        year_month = datetime.now().strftime("%Y/%m")

    ws = get_expense_sheet()
    all_values = ws.get_all_values()
    total = 0

    for row in all_values[1:]:
        if row[1].startswith(year_month) and row[13] != "cancelled":
            try:
                total += int(row[2])
            except (ValueError, IndexError):
                pass
    return total


def get_monthly_summary(year_month: str = None) -> dict:
    """月次サマリーを取得（事業別・科目別）"""
    if year_month is None:
        year_month = datetime.now().strftime("%Y/%m")

    ws = get_expense_sheet()
    all_values = ws.get_all_values()

    by_business = {}
    by_category = {}
    total = 0

    for row in all_values[1:]:
        if row[1].startswith(year_month) and row[13] != "cancelled":
            try:
                amount = int(row[2])
            except (ValueError, IndexError):
                continue

            total += amount

            biz_name = f"事業{row[7]}:{row[8]}"
            by_business[biz_name] = by_business.get(biz_name, 0) + amount

            cat_name = f"{row[5]}:{row[6]}"
            by_category[cat_name] = by_category.get(cat_name, 0) + amount

    return {
        "total": total,
        "by_business": dict(sorted(by_business.items())),
        "by_category": dict(sorted(by_category.items(), key=lambda x: -x[1])),
    }
