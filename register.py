import datetime
import pandas as pd
import googleapiclient.discovery
import google.auth


def register(date, time, summary, location):
    # 編集スコープの設定(今回は読み書き両方OKの設定)
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # カレンダーIDの設定(基本的には自身のgmailのアドレス)
    calendar_id = 'kubotadaiki0654@gmail.com'

    # 認証ファイルを使用して認証用オブジェクトを作成
    gapi_creds = google.auth.load_credentials_from_file(
        'credentials.json', SCOPES)[0]

    # 認証用オブジェクトを使用してAPIを呼び出すためのオブジェクト作成
    service = googleapiclient.discovery.build(
        'calendar', 'v3', credentials=gapi_creds)

    # 時限と時刻の対応リスト（最初2つが開始時刻、のこり2つが終了時刻）
    time_supported = [
        [9, 10, 10, 40],
        [10, 50, 12, 20],
        [13, 15, 14, 45],
        [14, 55, 16, 25],
        [16, 35, 18, 5]
    ]

    # データの前処理
    date = date.split("/")
    date = [int(i) for i in date]
    time = int(time)

    # 追加するスケジュールの情報を設定
    event = {
        # 予定のタイトル
        'summary': summary,
        # 予定の開始時刻(ISOフォーマットで指定)
        'start': {
            'dateTime': datetime.datetime(date[0], date[1], date[2], time_supported[time-1][0], time_supported[time-1][1]).isoformat(),
            'timeZone': 'Japan'
        },
        # 予定の終了時刻(ISOフォーマットで指定)
        'end': {
            'dateTime': datetime.datetime(date[0], date[1], date[2], time_supported[time-1][2], time_supported[time-1][3]).isoformat(),
            'timeZone': 'Japan'
        },
        'location': location,
        'recurrence': [
            'RRULE:FREQ=WEEKLY'
        ]
    }

    # 予定を追加する
    event = service.events().insert(calendarId=calendar_id, body=event).execute()


csvs = pd.read_csv('lecture.csv', header=0)

for csv in csvs.values:
    register(csv[0], csv[1], csv[2], csv[3])
