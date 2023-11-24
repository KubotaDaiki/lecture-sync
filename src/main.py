from certifi import contents
import flet as ft
from components.Button import Button, FilePickButton, DatePickButton
from components.Timetable import Timetable
from components.Modal import Modal
from utils import (
    get_client_storage,
    set_client_storage,
    set_init_value_to_client_storage,
)
import google.auth
import googleapiclient.discovery
from datetime import timedelta, datetime


def main(page: ft.Page):
    page.title = "Lecture Sync"
    page.theme_mode = "light"
    page.window_maximized = True
    page.window_min_width = 500

    set_init_value_to_client_storage(
        page,
        {
            "times": [
                ["9:10", "10:40"],
                ["10:50", "12:20"],
                ["13:15", "14:45"],
                ["14:55", "16:25"],
                ["16:35", "18:05"],
            ]
        },
    )
    storage_data = get_client_storage(page, ["gmail", "credentials_path", "times"])

    page.add(
        ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="予定入力",
                    icon=ft.icons.EDIT_CALENDAR,
                    content=MainTab(),
                ),
                ft.Tab(
                    text="設定",
                    icon=ft.icons.SETTINGS,
                    content=SettingTab(storage_data),
                ),
            ],
            expand=1,
        )
    )


class MainTab(ft.UserControl):
    def build(self):
        def get_date(e):
            self.tf_date.value = self.date_picker.value
            self.update()

        self.date_picker = DatePickButton("予定開始日を入力", get_date)
        self.tf_date = ft.TextField(width=300)
        self.timetable = TimetableWithModal()
        self.registration_button = RegistrationButtonWithModal(
            self.timetable, self.tf_date
        )
        return ft.Column(
            [
                ft.Row(
                    [
                        self.date_picker,
                        self.tf_date,
                    ],
                    alignment="CENTER",
                ),
                self.timetable,
                self.registration_button,
            ],
            spacing=20,
            scroll="AUTO",
            horizontal_alignment="CENTER",
        )


class TimetableWithModal(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.schedules = {}
        self.lecture_title = ft.TextField(label="講義名", autofocus=True)
        self.place = ft.TextField(label="場所")
        self.input_modal = Modal(
            contents=[self.lecture_title, self.place],
            on_click=self.register_for_timetable,
            close_modal=self.close_input_modal,
        )

    def register_for_timetable(self):
        self.card.card.content = ft.Text(
            f"{self.lecture_title.value}\n{self.place.value}"
        )
        self.card.update()
        self.schedules[self.card.label] = {
            "lecture_title": self.lecture_title.value,
            "place": self.place.value,
        }

    def close_input_modal(self, e):
        for content in self.input_modal.contents:
            content.value = ""
        self.input_modal.alert.open = False
        self.input_modal.update()

    def did_mount(self):
        if self.page is None:
            return

        self.page.overlay.append(self.input_modal)
        self.page.update()

    def open_input_modal(self, card):
        WEEKS = ["月", "火", "水", "木", "金", "土", "日"]
        self.card = card
        period_idx, week_idx = int(card.label[0]), int(card.label[1])
        self.input_modal.title = f"予定を入力（{WEEKS[week_idx]}曜{period_idx+1}限）"
        self.input_modal.open = True
        self.input_modal.update()

    def build(self):
        self.timetable = Timetable(self.open_input_modal)
        return self.timetable


class RegistrationButtonWithModal(ft.UserControl):
    def __init__(self, timetable, tf_date):
        super().__init__()
        self.register_text = ft.Text("時間割をGoogleカレンダーに登録しますか？")
        self.progress_bar = ft.ProgressBar(width=400, visible=False)
        self.register_modal = Modal(
            contents=[self.register_text, self.progress_bar],
            on_click=self.register_on_google_calendar,
            close_modal=self.close_modal,
            title="Googleカレンダーに登録",
        )
        self.timetable = timetable
        self.tf_date = tf_date

    def register_on_google_calendar(self):
        self.progress_bar.visible = True
        self.register_modal.update()

        storage_data = get_client_storage(
            self.page,
            ["gmail", "credentials_path", "times"],
        )

        SCOPES = ["https://www.googleapis.com/auth/calendar"]
        gapi_creds = google.auth.load_credentials_from_file(
            storage_data["credentials_path"], SCOPES
        )[0]
        service = googleapiclient.discovery.build(
            "calendar",
            "v3",
            credentials=gapi_creds,
            static_discovery=False,
        )

        for key, input_data in self.timetable.schedules.items():
            period_idx, week_idx = int(key[0]), int(key[1])
            if (input_data["lecture_title"] == "") and (input_data["place"] == ""):
                continue

            date = self.tf_date.value + timedelta(days=week_idx)
            start_time = datetime.strptime(
                storage_data["times"][period_idx][0], "%H:%M"
            ).time()
            start_date = datetime.combine(date, start_time)
            end_time = datetime.strptime(
                storage_data["times"][period_idx][1], "%H:%M"
            ).time()
            end_date = datetime.combine(date, end_time)
            event = {
                "summary": input_data["lecture_title"],
                "start": {
                    "dateTime": start_date.isoformat(),
                    "timeZone": "Japan",
                },
                "end": {
                    "dateTime": end_date.isoformat(),
                    "timeZone": "Japan",
                },
                "location": input_data["place"],
                "recurrence": ["RRULE:FREQ=WEEKLY"],
            }
            event = (
                service.events()
                .insert(calendarId=storage_data["gmail"], body=event)
                .execute()
            )

    def close_modal(self, e):
        self.progress_bar.visible = False
        self.register_modal.alert.open = False
        self.register_modal.update()

    def did_mount(self):
        if self.page is None:
            return

        self.page.overlay.append(self.register_modal)
        self.page.update()

    def open_register_modal(self, e):
        self.register_modal.open = True
        self.register_modal.update()

    def build(self):
        return Button(
            "Googleカレンダーに登録", icon="calendar_month", on_click=self.open_register_modal
        )


class SettingTab(ft.UserControl):
    def __init__(self, storage_data):
        super().__init__()
        self.storage_data = storage_data

    def did_mount(self):
        if self.page is None:
            return

        self.page.overlay.append(self.credentials_path.file_dialog)
        self.page.update()

    def add_setting(self, e):
        if self.page is None:
            return

        times = [
            [t.controls[0].value, t.controls[1].value] for t in self.times.controls
        ]

        set_client_storage(
            self.page,
            {
                "gmail": self.gmail.value,
                "credentials_path": self.credentials_path.value,
                "times": times,
            },
        )
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("登録完了しました"),
        )
        self.page.snack_bar.open = True
        self.page.update()

    def build(self):
        self.credentials_path = FilePickButton(
            field_label="認証ファイルのパス",
            button_text="認証ファイルを選択",
            value=self.storage_data["credentials_path"],
        )
        self.gmail = ft.TextField(label="Gmail", value=self.storage_data["gmail"])
        self.button = Button("情報を登録", "save", self.add_setting)

        self.times = ft.Column()
        for i, (start, end) in enumerate(self.storage_data["times"]):
            self.times.controls.append(
                ft.Row(
                    controls=[
                        ft.TextField(label=f"{i+1}限 開始時刻", value=start),
                        ft.TextField(label=f"{i+1}限 終了時刻", value=end),
                    ],
                )
            )

        return ft.Container(
            ft.Column(
                [
                    ft.Text("Googleカレンダー用認証情報の設定", style=ft.TextThemeStyle.TITLE_LARGE),
                    self.gmail,
                    self.credentials_path,
                    ft.Text("時刻の設定", style=ft.TextThemeStyle.TITLE_LARGE),
                    self.times,
                    self.button,
                ],
                spacing=30,
                scroll="AUTO",
            ),
            margin=ft.margin.symmetric(vertical=40, horizontal=20),
        )


if __name__ == "__main__":
    ft.app(target=main)
