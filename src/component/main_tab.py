import calendar
import itertools
from datetime import time, timedelta, date, datetime

import flet as ft
import google.auth
import googleapiclient.discovery
from dateutil.relativedelta import relativedelta


WEEKS = ["月", "火", "水", "木", "金", "土", "日"]
schedules = {}


class DatePiker(ft.UserControl):
    def __init__(self, on_selected=None):
        super().__init__()
        self.default_date = date.today()
        self.yearmonth = date(self.default_date.year, self.default_date.month, 1)
        self.selected_date = self.default_date
        self.on_selected = on_selected

    def build(self):
        DAY_WIDTH = 36
        DAY_SPACING = 4

        def updateCalender():
            """カレンダーの中身を更新する"""

            # ヘッダの年月設定
            self.txt_yearmonth.value = self.yearmonth.strftime("%Y/%m")

            # 日付のボタンを全部クリア
            for idx in range(42):  # 7日×6週
                self.btn_days[idx].text = "-"
                self.btn_days[idx].disabled = True
                self.btn_days[idx].style = ft.ButtonStyle(
                    padding=0, bgcolor=ft.colors.BACKGROUND
                )

            # カレンダー情報取得
            list_cal = list(
                itertools.chain.from_iterable(
                    calendar.monthcalendar(self.yearmonth.year, self.yearmonth.month)
                )
            )

            # カレンダー情報を日付のボタンに設定
            idx = 0
            for day in list_cal:
                if day > 0:
                    self.btn_days[idx].text = day
                    self.btn_days[idx].disabled = False
                    if (
                        date(self.yearmonth.year, self.yearmonth.month, day)
                        == self.selected_date
                    ):
                        self.btn_days[idx].style = ft.ButtonStyle(
                            padding=0, bgcolor=ft.colors.TRANSPARENT
                        )
                idx = idx + 1

        def prev_clicked(e):
            self.yearmonth = self.yearmonth - relativedelta(months=1)
            updateCalender()
            self.update()

        def next_clicked(e):
            self.yearmonth = self.yearmonth + relativedelta(months=1)
            updateCalender()
            self.update()

        def today_clicked(e):
            self.yearmonth = date.today()
            self.selected_date = date.today()
            updateCalender()
            self.update()

        def day_clicked(e):
            day = e.control.text
            self.selected_date = date(self.yearmonth.year, self.yearmonth.month, day)
            updateCalender()
            self.update()
            if self.on_selected:
                self.on_selected()

        # I/O Controls
        self.btn_prev = ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=prev_clicked)
        self.btn_next = ft.IconButton(
            icon=ft.icons.ARROW_FORWARD, on_click=next_clicked
        )
        self.txt_yearmonth = ft.Text(
            self.yearmonth.strftime("%Y/%m"), size=24, weight=ft.FontWeight.BOLD
        )
        self.btn_today = ft.ElevatedButton("今日", on_click=today_clicked)
        self.btn_days = []
        week_cols = []
        for week in range(6):
            # 6週分の行を追加
            calenderRows = []
            for day in range(7):
                # 7日分のボタンを追加
                btn_day = ft.ElevatedButton(
                    width=DAY_WIDTH,
                    style=ft.ButtonStyle(padding=0),
                    on_click=day_clicked,
                )
                self.btn_days.append(btn_day)
                calenderRows.append(btn_day)
            week_cols.append(
                ft.Row(
                    controls=calenderRows,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=DAY_SPACING,
                )
            )
        updateCalender()

        return ft.Column(
            [
                # ヘッダ
                ft.Row(
                    [
                        self.btn_prev,
                        self.txt_yearmonth,
                        self.btn_next,
                        self.btn_today,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                # カレンダーヘッダ
                ft.Row(
                    [
                        ft.Text("月", width=DAY_WIDTH, text_align=ft.TextAlign.CENTER),
                        ft.Text("火", width=DAY_WIDTH, text_align=ft.TextAlign.CENTER),
                        ft.Text("水", width=DAY_WIDTH, text_align=ft.TextAlign.CENTER),
                        ft.Text("木", width=DAY_WIDTH, text_align=ft.TextAlign.CENTER),
                        ft.Text("金", width=DAY_WIDTH, text_align=ft.TextAlign.CENTER),
                        ft.Text(
                            "土",
                            width=DAY_WIDTH,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.BLUE,
                        ),
                        ft.Text(
                            "日",
                            width=DAY_WIDTH,
                            text_align=ft.TextAlign.CENTER,
                            color=ft.colors.RED,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=DAY_SPACING,
                ),
                # カレンダー内容
                ft.Row(
                    [
                        ft.Column(
                            controls=week_cols,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ]
        )


class CalendarModal(ft.UserControl):
    def __init__(self, calender_set, dialog):
        super().__init__()
        self.datepicker = DatePiker(on_selected=self.date_selected)
        self.calender_set = calender_set
        self.dialog = dialog

    def open_dlg(self, e):
        self.dialog = self.modal
        self.modal.open = True
        self.modal.update()

    def date_selected(self):
        self.calender_set.value = self.datepicker.selected_date.strftime("%Y/%m/%d")
        self.modal.open = False
        self.modal.update()
        self.calender_set.update()

    def build(self):
        card = ft.Card(
            ft.Container(
                self.datepicker,
                margin=10,
                width=300,
                height=330,
            )
        )
        self.modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("予定開始日を入力"),
            content=card,
            actions_alignment=ft.MainAxisAlignment.END,
            content_padding=ft.padding.only(50, 20, 50, 20),
        )
        return self.modal


class Calendar(ft.UserControl):
    def __init__(self, dialog):
        super().__init__()
        self.modal = CalendarModal(self, dialog)

    def build(self):
        self.tf_date = ft.TextField(width=300)
        btn_calender = ft.ElevatedButton(
            text="予定開始日",
            on_click=self.modal.open_dlg,
            width=200,
            height=50,
            icon="calendar_month",
        )

        return ft.Container(
            ft.Row(
                [
                    btn_calender,
                    self.tf_date,
                ],
                alignment="CENTER",
            ),
            margin=ft.margin.only(top=50, bottom=20),
        )

    @property
    def value(self):
        return self.tf_date.value

    @value.setter
    def value(self, value):
        self.tf_date.value = value


class InputModal(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.column = []
        self.content = []
        self.alert = ft.AlertDialog(
            modal=True,
            title=ft.Text("予定を入力"),
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.alert.actions = [
            ft.TextButton("登録", on_click=self.register),
            ft.TextButton("キャンセル", on_click=self.close_dlg),
        ]

    def close_dlg(self, e):
        self.alert.open = False
        self.alert.update()

    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.key == "Escape":
            self.close_dlg(e)

    def register(self, e):
        self.column[1] = ft.Text(f"{self.lecture_title.value}\n{self.place.value}")
        self.content.update()
        schedules[self.col0] = [self.lecture_title.value, self.place.value]
        self.close_dlg(e)

    def build(self):
        return self.alert

    def open(self):
        self.col0 = self.column[0].value
        self.lecture_title = ft.TextField(label="講義名", autofocus=True)
        self.place = ft.TextField(label="場所")

        self.alert.content = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"{WEEKS[int(self.col0[0])]}曜{int(self.col0[1])+1}限", size=20
                    ),
                    self.lecture_title,
                    self.place,
                ]
            ),
            alignment=ft.alignment.center,
            width=500,
            height=500,
        )


class Timetable(ft.UserControl):
    def __init__(self, dialog, on_keyboard_event):
        super().__init__()
        self.dialog = dialog
        self.on_keyboard_event = on_keyboard_event
        self.modal = InputModal()

    def open_dlg_modal(self, e):
        self.modal.column = e.control.content.controls
        self.modal.content = e.control.content
        self.modal.open()
        self.on_keyboard_event = self.modal.on_keyboard
        self.dialog = self.modal.alert
        self.modal.alert.open = True
        self.modal.alert.update()

    def build(self):
        def on_hover(e):
            e.control.bgcolor = ft.colors.BLUE if e.data == "true" else ft.colors.WHITE
            e.control.update()

        timetable = []
        timetable.append(
            ft.Row(
                [
                    Card(
                        ft.Text(week, color=ft.colors.WHITE), bgcolor=ft.colors.BLUE_400
                    )
                    for week in ["", *WEEKS]
                ],
                alignment="CENTER",
            )
        )

        for i in range(5):
            rows = []
            rows.append(
                Card(
                    ft.Text(f"{i+1}限", color=ft.colors.WHITE),
                    bgcolor=ft.colors.BLUE_400,
                )
            )
            for j in range(7):
                rows.append(
                    Card(
                        ft.Column(
                            [
                                ft.Text(f"{j}{i}", visible=False),
                                ft.Text(f"{j}{i}", visible=False),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        on_click=self.open_dlg_modal,
                        on_hover=on_hover,
                    )
                )
            timetable.append(ft.Row(rows, alignment="CENTER"))
        return ft.Column(controls=timetable)


class Card(ft.UserControl):
    def __init__(self, content, on_click=None, on_hover=None, bgcolor=ft.colors.WHITE):
        super().__init__()
        self.card = ft.Container(
            content=content,
            alignment=ft.alignment.center,
            width=120,
            height=100,
            padding=10,
            bgcolor=bgcolor,
            border_radius=ft.border_radius.all(5),
            on_click=on_click,
            on_hover=on_hover,
            border=ft.border.all(1, ft.colors.BLUE_300),
        )

    def build(self):
        return self.card


class RegisterModal(ft.UserControl):
    def __init__(self, register, close_dlg):
        super().__init__()
        self.modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Googleカレンダーに登録"),
            actions=[
                ft.TextButton("登録", on_click=register),
                ft.TextButton("キャンセル", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def build(self):
        return self.modal


class RegistrationButton(ft.UserControl):
    def __init__(self, datepicker, gmail, credentials_path, dialog):
        super().__init__()
        self.register = RegisterModal(self.register_in_calendar, self.close_dlg)
        self.datepicker = datepicker
        self.gmail = gmail
        self.credentials_path = credentials_path
        self.dialog = dialog

    def build(self):
        return ft.Container(
            ft.ElevatedButton(
                "Googleカレンダーに登録",
                height=50,
                width=300,
                icon="calendar_month",
                on_click=self.open_dlg,
                style=ft.ButtonStyle(
                    color={
                        ft.MaterialState.DEFAULT: ft.colors.WHITE,
                    },
                    bgcolor={
                        ft.MaterialState.DEFAULT: ft.colors.BLUE_700,
                        ft.MaterialState.HOVERED: ft.colors.BLUE_900,
                    },
                    shape=ft.RoundedRectangleBorder(radius=20),
                ),
            ),
            margin=30,
        )

    def register_in_calendar(self, e):
        self.register_(
            schedules,
            self.datepicker.selected_date,
            self.gmail_value,
            self.credentials_path_value,
        )
        self.close_dlg()

    def open_dlg(self, e):
        self.gmail_value = self.gmail.value
        self.credentials_path_value = self.credentials_path.value

        self.dialog = self.register.modal
        self.register.modal.open = True
        self.register.modal.update()

    def close_dlg(self):
        self.register.modal.open = False
        self.register.modal.update()

    def register_(self, schedules, date, calendar_id, credentials_path):
        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        gapi_creds = google.auth.load_credentials_from_file(credentials_path, SCOPES)[0]
        service = googleapiclient.discovery.build(
            "calendar", "v3", credentials=gapi_creds, static_discovery=False
        )

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
                date_delta,
                time(end_time[time_idx]["hour"], end_time[time_idx]["minute"]),
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
            event = (
                service.events().insert(calendarId=calendar_id, body=event).execute()
            )
