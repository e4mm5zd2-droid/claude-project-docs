from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    date: str                    # YYYY/MM/DD
    amount: int                  # 税込金額（円）
    tax_amount: int              # 消費税額（円）
    store_name: str              # 店名/支払先
    category_code: str           # 勘定科目コード（01-99）
    category_name: str           # 勘定科目名
    business_number: str         # 事業番号（0-4）
    business_name: str           # 事業名
    memo: str = ""               # 備考
    registration_method: str = "manual"  # photo / text / manual
    image_file_id: str = ""      # Telegram file_id
    registered_at: str = field(default_factory=lambda: datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    status: str = "pending"      # pending / confirmed / corrected
    expense_id: str = ""         # EXP-YYYYMMDD-NNN

    def to_sheet_row(self) -> list:
        """Google Sheetsの1行に変換"""
        return [
            self.expense_id,
            self.date,
            self.amount,
            self.tax_amount,
            self.store_name,
            self.category_code,
            self.category_name,
            self.business_number,
            self.business_name,
            self.memo,
            self.registration_method,
            self.image_file_id,
            self.registered_at,
            self.status,
        ]

    def to_confirmation_message(self, monthly_total: int = 0) -> str:
        """Telegram確認メッセージを生成"""
        msg = (
            "✅ 登録完了\n"
            "━━━━━━━━━━\n"
            f"📅 {self.date}\n"
            f"💰 ¥{self.amount:,}\n"
            f"🏪 {self.store_name}\n"
            f"📂 {self.category_code}:{self.category_name}\n"
            f"🏢 事業{self.business_number}:{self.business_name}\n"
        )
        if self.memo:
            msg += f"📝 {self.memo}\n"
        msg += (
            "━━━━━━━━━━\n"
            "修正 → 数字で返信\n"
            "1:日付 2:金額 3:店名 4:科目 5:事業\n"
            "━━━━━━━━━━\n"
        )
        if monthly_total > 0:
            msg += f"今月累計: ¥{monthly_total:,}"
        return msg
