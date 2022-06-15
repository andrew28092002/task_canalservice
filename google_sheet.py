from __future__ import print_function
import os.path
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleSheet:
    # id таблицы Google Sheets
    SPREADSHEET_ID = '1oIsxuNf_F8MH1XY5hcw15DWXZXmC0LwExZaIlC9W69o'
    # Уровень доступа для чтения/записи/форматирования
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    service = None

    def __init__(self):
        creds = None
        # Если токен сгенерирован, то берется из директории
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # Если токена нет или есть ошибка
        if not creds or not creds.valid:
            # обновление токена
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('sheets', 'v4', credentials=creds)

    # Метод записи значений в таблицы
    def updateRangeValues(self, range, values):
        data = [{
            'range': range,
            'values': values
        }]
        body = {
            'valueInputOption': 'USER_ENTERED',
            'data': data
        }
        result = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.SPREADSHEET_ID,
                                                                  body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))

    # Метод получения значений из таблицы
    def get_values(self, range):
        result = self.service.spreadsheets().values().batchGet(spreadsheetId=self.SPREADSHEET_ID,
                                                               ranges=range).execute()
        return result.get('valueRanges')[0].get('values')[1:]
