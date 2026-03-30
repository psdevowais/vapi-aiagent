import json
import os
from dataclasses import dataclass
from typing import Optional

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


@dataclass(frozen=True)
class GoogleSheetsConfig:
    spreadsheet_id: str
    worksheet_name: str
    service_account_json: dict


def _load_config() -> Optional[GoogleSheetsConfig]:
    spreadsheet_id = os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID', '').strip()
    if not spreadsheet_id:
        return None

    worksheet_name = os.environ.get('GOOGLE_SHEETS_WORKSHEET_NAME', 'Leads').strip() or 'Leads'

    raw_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON', '').strip()
    if not raw_json:
        return None

    service_account_json = json.loads(raw_json)

    return GoogleSheetsConfig(
        spreadsheet_id=spreadsheet_id,
        worksheet_name=worksheet_name,
        service_account_json=service_account_json,
    )


def append_lead_row(values: list[str]) -> None:
    config = _load_config()
    if not config:
        return

    creds = Credentials.from_service_account_info(
        config.service_account_json,
        scopes=['https://www.googleapis.com/auth/spreadsheets'],
    )

    service = build('sheets', 'v4', credentials=creds)
    sheets = service.spreadsheets()

    sheets.values().append(
        spreadsheetId=config.spreadsheet_id,
        range=f"{config.worksheet_name}!A1",
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': [values]},
    ).execute()
