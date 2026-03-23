import anthropic
import base64
import json
import re
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CATEGORIES, BUSINESSES

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """あなたは日本の法人経費管理アシスタントです。
領収書の画像を解析し、以下のJSON形式で情報を抽出してください。

出力形式（JSONのみ、他のテキストは不要）：
{
    "date": "YYYY/MM/DD",
    "amount": 金額（税込、整数）,
    "tax_amount": 消費税額（整数、不明なら税込金額×10/110で計算）,
    "store_name": "店名/支払先",
    "category_code": "勘定科目コード（下記参照）",
    "category_name": "勘定科目名",
    "business_number": "事業番号（下記参照）",
    "memo": "備考（読み取れない部分や特記事項）"
}

勘定科目コード：
01:通信費, 02:広告宣伝費, 03:旅費交通費, 04:接待交際費,
05:消耗品費, 06:支払手数料, 07:外注費, 08:地代家賃,
09:水道光熱費, 10:新聞図書費, 11:諸会費, 12:租税公課,
13:保険料, 14:減価償却費, 15:研修費, 99:雑費

事業番号：0:全社, 1:アフィリ, 2:Xツール, 3:求人, 4:CRM

判断基準：
- 飲食店 → 04:接待交際費（デフォルト）
- 交通系 → 03:旅費交通費
- Amazon/ヨドバシ等 → 05:消耗品費
- サーバー/API/ドメイン → 01:通信費
- 事業番号が判断できない場合は0（全社）
- 日付が読み取れない場合は今日の日付
- 金額が読み取れない場合は0として、memoに「金額要確認」と記載
"""


async def analyze_receipt(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """領収書画像をClaude Vision APIで解析"""
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": base64_image,
                        },
                    },
                    {
                        "type": "text",
                        "text": "この領収書を解析してJSON形式で返してください。",
                    },
                ],
            }
        ],
    )

    # レスポンスからJSONを抽出
    response_text = message.content[0].text
    # ```json ... ``` のフェンスを除去
    cleaned = re.sub(r"```json\s*", "", response_text)
    cleaned = re.sub(r"```\s*", "", cleaned)
    cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        result = {
            "date": "",
            "amount": 0,
            "tax_amount": 0,
            "store_name": "解析失敗",
            "category_code": "99",
            "category_name": "雑費",
            "business_number": "0",
            "memo": "OCR解析に失敗しました。手動入力してください。",
        }

    # バリデーション
    if result.get("category_code") not in CATEGORIES:
        result["category_code"] = "99"
        result["category_name"] = "雑費"

    if result.get("business_number") not in BUSINESSES:
        result["business_number"] = "0"

    return result
