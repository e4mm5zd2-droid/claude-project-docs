import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload
from google.oauth2.service_account import Credentials
from datetime import datetime
from config import GOOGLE_SERVICE_ACCOUNT_JSON

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
]

credentials = Credentials.from_service_account_file(
    GOOGLE_SERVICE_ACCOUNT_JSON, scopes=SCOPES
)
drive_service = build("drive", "v3", credentials=credentials)

ROOT_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")


def get_or_create_month_folder(year_month: str) -> str:
    """YYYY-MM形式のサブフォルダを取得or作成"""
    query = (
        f"name='{year_month}' and "
        f"'{ROOT_FOLDER_ID}' in parents and "
        f"mimeType='application/vnd.google-apps.folder' and trashed=false"
    )
    results = drive_service.files().list(q=query, fields="files(id)").execute()
    files = results.get("files", [])

    if files:
        return files[0]["id"]

    folder_metadata = {
        "name": year_month,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [ROOT_FOLDER_ID],
    }
    folder = drive_service.files().create(
        body=folder_metadata, fields="id"
    ).execute()
    return folder["id"]


def upload_receipt(image_bytes: bytes, expense_id: str, mime_type: str = "image/jpeg") -> str:
    """領収書画像をDriveにアップロード、公開URLを返す"""
    year_month = datetime.now().strftime("%Y-%m")
    folder_id = get_or_create_month_folder(year_month)

    ext = "jpg" if "jpeg" in mime_type else "png"
    file_metadata = {
        "name": f"{expense_id}.{ext}",
        "parents": [folder_id],
    }
    media = MediaInMemoryUpload(image_bytes, mimetype=mime_type)
    file = drive_service.files().create(
        body=file_metadata, media_body=media, fields="id,webViewLink"
    ).execute()

    return file.get("webViewLink", "")
