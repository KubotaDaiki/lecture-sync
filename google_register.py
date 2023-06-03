import datetime
import googleapiclient.discovery
import google.auth
from datetime import datetime, date, time, timedelta


def register(schedules, date, calendar_id, credentials_path):
    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    gapi_creds = google.auth.load_credentials_from_file(credentials_path, SCOPES)[0]
    service = googleapiclient.discovery.build("calendar", "v3", credentials=gapi_creds)

    start_time = [
        {"hour": 9, "minute": 10},
        {"hour": 10, "minute": 50},
        {"hour": 13, "minute": 15},
        {"hour": 14, "minute": 55},
        {"hour": 16, "minute": 35},
    ]
    end_time = [
        {"hour": 10, "minute": 40},
        {"hour": 12, "minute": 20},
        {"hour": 14, "minute": 45},
        {"hour": 16, "minute": 25},
        {"hour": 18, "minute": 5},
    ]
    for key, value in schedules.items():
        if (value[0] == "") and (value[1] == ""):
            continue
        date_delta = date + timedelta(days=int(key[0]))
        time_idx = int(key[1])
        start_date = datetime.combine(
            date_delta,
            time(start_time[time_idx]["hour"], start_time[time_idx]["minute"]),
        )
        end_date = datetime.combine(
            date_delta, time(end_time[time_idx]["hour"], end_time[time_idx]["minute"])
        )
        event = {
            "summary": value[0],
            "start": {
                "dateTime": start_date.isoformat(),
                "timeZone": "Japan",
            },
            "end": {
                "dateTime": end_date.isoformat(),
                "timeZone": "Japan",
            },
            "location": value[1],
            "recurrence": ["RRULE:FREQ=WEEKLY"],
        }
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
