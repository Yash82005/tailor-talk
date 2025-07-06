import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'primary'


if "GOOGLE_SERVICE_ACCOUNT" in os.environ:
    service_account_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT"])
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES
    )
else:
    credentials = service_account.Credentials.from_service_account_file(
        'backend/service_account.json', scopes=SCOPES
    )


service = build('calendar', 'v3', credentials=credentials)

def get_free_slots():
    now = datetime.utcnow().isoformat() + 'Z'
    later = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        timeMax=later,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return events

def create_event(start, end, summary):
    event = {
        'summary': summary,
        'start': {'dateTime': start, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end, 'timeZone': 'Asia/Kolkata'}
    }

    event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return event.get('htmlLink')
