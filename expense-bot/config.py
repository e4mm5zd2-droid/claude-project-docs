import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_IDS = [int(uid.strip()) for uid in os.getenv("ALLOWED_USER_IDS", "").split(",") if uid.strip()]

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
CLAUDE_MODEL = "claude-sonnet-4-20250514"

# Google Sheets
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
GOOGLE_SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "service_account.json")

# 勘定科目マスター
CATEGORIES = {
    "01": "通信費",
    "02": "広告宣伝費",
    "03": "旅費交通費",
    "04": "接待交際費",
    "05": "消耗品費",
    "06": "支払手数料",
    "07": "外注費",
    "08": "地代家賃",
    "09": "水道光熱費",
    "10": "新聞図書費",
    "11": "諸会費",
    "12": "租税公課",
    "13": "保険料",
    "14": "減価償却費",
    "15": "研修費",
    "99": "雑費",
}

# 事業マスター
BUSINESSES = {
    "0": "全社",
    "1": "アフィリ",
    "2": "Xツール",
    "3": "求人",
    "4": "CRM",
}

# 予算設定（暫定値・BUDGET_ALERT_ENABLEDをTrueにすると有効化）
BUDGET_ALERT_ENABLED = False
MONTHLY_BUDGETS = {
    "0": 50000, "1": 30000, "2": 50000, "3": 250000, "4": 20000,
}
TOTAL_MONTHLY_BUDGET = 400000
ALERT_THRESHOLD = 0.8
