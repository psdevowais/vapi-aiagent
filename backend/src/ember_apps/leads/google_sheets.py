import os
from datetime import timedelta
from urllib.parse import urlencode

import requests
from django.utils import timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .oauth_models import GoogleOAuthToken


SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/gmail.send',
]


def get_client_config():
    client_id = os.environ.get('GOOGLE_CLIENT_ID', '').strip()
    client_secret = os.environ.get('GOOGLE_CLIENT_SECRET', '').strip()
    if not client_id or not client_secret:
        return None
    return {
        'client_id': client_id,
        'client_secret': client_secret,
    }


def get_authorization_url():
    config = get_client_config()
    if not config:
        return None

    redirect_uri = os.environ.get(
        'GOOGLE_REDIRECT_URI',
        'http://127.0.0.1:8000/api/auth/google/callback/'
    )

    params = {
        'client_id': config['client_id'],
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'prompt': 'consent',
    }

    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"


def exchange_code_for_tokens(code: str) -> dict | None:
    config = get_client_config()
    if not config:
        return None

    redirect_uri = os.environ.get(
        'GOOGLE_REDIRECT_URI',
        'http://127.0.0.1:8000/api/auth/google/callback/'
    )

    response = requests.post(
        'https://oauth2.googleapis.com/token',
        data={
            'code': code,
            'client_id': config['client_id'],
            'client_secret': config['client_secret'],
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code',
        },
        timeout=30,
    )

    if response.status_code != 200:
        return None

    return response.json()


def get_or_refresh_credentials() -> Credentials | None:
    try:
        token_obj = GoogleOAuthToken.objects.get(id=1)
    except GoogleOAuthToken.DoesNotExist:
        return None

    config = get_client_config()
    if not config:
        return None

    if token_obj.expires_at and timezone.now() >= token_obj.expires_at:
        response = requests.post(
            'https://oauth2.googleapis.com/token',
            data={
                'refresh_token': token_obj.refresh_token,
                'client_id': config['client_id'],
                'client_secret': config['client_secret'],
                'grant_type': 'refresh_token',
            },
            timeout=30,
        )

        if response.status_code != 200:
            return None

        token_data = response.json()
        token_obj.access_token = token_data['access_token']
        expires_in = token_data.get('expires_in', 3600)
        token_obj.expires_at = timezone.now() + timedelta(seconds=expires_in - 60)
        token_obj.save(update_fields=['access_token', 'expires_at', 'updated_at'])

    return Credentials(
        token=token_obj.access_token,
        refresh_token=token_obj.refresh_token,
        token_uri=token_obj.token_uri,
        client_id=token_obj.client_id,
        client_secret=token_obj.client_secret,
        scopes=SCOPES,
    )


def append_lead_row(values: list[str]) -> None:
    spreadsheet_id = os.environ.get('GOOGLE_SHEETS_SPREADSHEET_ID', '').strip()
    if not spreadsheet_id:
        return

    creds = get_or_refresh_credentials()
    if not creds:
        return

    service = build('sheets', 'v4', credentials=creds)
    sheets = service.spreadsheets()

    worksheet_name = os.environ.get('GOOGLE_SHEETS_WORKSHEET_NAME', 'Leads').strip() or 'Leads'

    sheets.values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{worksheet_name}!A1",
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body={'values': [values]},
    ).execute()


def send_urgent_lead_email(lead_data: dict) -> bool:
    admin_email = os.environ.get('ADMIN_EMAIL', '').strip()
    if not admin_email:
        return False

    creds = get_or_refresh_credentials()
    if not creds:
        return False

    import base64
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    service = build('gmail', 'v1', credentials=creds)

    message = MIMEMultipart('alternative')
    message['To'] = admin_email
    message['Subject'] = f"Urgent Lead: {lead_data.get('customer_name', 'New Lead')}"

    html_body = f"""
    <html>
      <body>
        <h2>Urgent Lead Notification</h2>
        <table style="border-collapse: collapse; width: 100%;">
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Customer Name</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{lead_data.get('customer_name', 'N/A')}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Phone</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{lead_data.get('phone', 'N/A')}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Email</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{lead_data.get('email', 'N/A')}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Property Address</strong></td><td style="padding: 8px; border: 1px solid #ddd;">{lead_data.get('property_address', 'N/A')}</td></tr>
          <tr><td style="padding: 8px; border: 1px solid #ddd;"><strong>Priority</strong></td><td style="padding: 8px; border: 1px solid #ddd; color: red; font-weight: bold;">{lead_data.get('call_priority', 'N/A')}</td></tr>
        </table>
        <p style="margin-top: 16px;">This lead has been automatically synced to Google Sheets.</p>
      </body>
    </html>
    """

    text_body = f"""
Urgent Lead Notification

Customer Name: {lead_data.get('customer_name', 'N/A')}
Phone: {lead_data.get('phone', 'N/A')}
Email: {lead_data.get('email', 'N/A')}
Property Address: {lead_data.get('property_address', 'N/A')}
Priority: {lead_data.get('call_priority', 'N/A')}

This lead has been automatically synced to Google Sheets.
    """

    part1 = MIMEText(text_body, 'plain')
    part2 = MIMEText(html_body, 'html')
    message.attach(part1)
    message.attach(part2)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    try:
        service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        return True
    except Exception:
        return False
