import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]
SHEET_ID = "1srJqGWA5pO4MqXquVSqUOv6VEcmotI1lolMy3VaNl3o"
CREDENTIALS_FILE = "credentials.json"


def get_gspread_client():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def list_sheets():
    gc = get_gspread_client()
    sh = gc.open_by_key(SHEET_ID)
    return [(ws.title, ws.id) for ws in sh.worksheets()]


def get_sheet_as_df(sheet_name: str) -> pd.DataFrame:
    gc = get_gspread_client()
    sh = gc.open_by_key(SHEET_ID)
    ws = sh.worksheet(sheet_name)
    data = ws.get_all_values()
    if not data:
        return pd.DataFrame()
    headers = data[0]
    rows = data[1:]
    return pd.DataFrame(rows, columns=headers)


def get_all_sheets_raw() -> dict:
    """Returns all worksheets as a dict of {sheet_name: raw_values_list}"""
    gc = get_gspread_client()
    sh = gc.open_by_key(SHEET_ID)
    result = {}
    for ws in sh.worksheets():
        result[ws.title] = ws.get_all_values()
    return result
