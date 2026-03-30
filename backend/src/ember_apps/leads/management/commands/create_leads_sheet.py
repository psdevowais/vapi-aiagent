import json
import os

from django.core.management.base import BaseCommand, CommandError
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


class Command(BaseCommand):
    help = 'Create a new Google Spreadsheet for leads and print its spreadsheet_id'

    def handle(self, *args, **options):
        raw_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON', '').strip()
        if not raw_json:
            raise CommandError('GOOGLE_SERVICE_ACCOUNT_JSON is required')

        service_account_json = json.loads(raw_json)
        creds = Credentials.from_service_account_info(
            service_account_json,
            scopes=['https://www.googleapis.com/auth/spreadsheets'],
        )

        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = (
            service.spreadsheets()
            .create(body={'properties': {'title': 'Ember Homes Leads'}})
            .execute()
        )

        spreadsheet_id = spreadsheet.get('spreadsheetId')
        if not spreadsheet_id:
            raise CommandError('Failed to create spreadsheet')

        self.stdout.write(spreadsheet_id)
