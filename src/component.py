import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import itertools
import google_register

WEEKS = ["月", "火", "水", "木", "金", "土", "日"]
schedules = {}


class DatePiker(ft.UserControl):
    def __init__(self, on_selected=None):
        super().__init__()
        self.default_date = datetime.date.today()
        self.yearmonth: datetime = datetime.date(
            self.default_date.year, self.default_date.month, 1
        )
        self.selected_date: datetime = self.default_date
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
                        datetime.date(self.yearmonth.year, self.yearmonth.month, day)
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
            self.yearmonth = datetime.date.today()
            self.selected_date = datetime.date.today()
            updateCalender()
            self.update()

        def day_clicked(e):
            day = e.control.text
            self.selected_date = datetime.date(
                self.yearmonth.year, self.yearmonth.month, day
            )
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

    def update(self):
        super().update()


class SettingGmail(ft.UserControl):
    def __init__(self, gmail: str):
        """設定タブのGmail欄のコンポーネント

        Parameters
        ----------
        gmail : str
            ストレージに保存されているgmailアドレス
        """
        super().__init__()
        self.gmail = ft.TextField(label="Gmail", value=gmail)

    def build(self):
        return self.gmail

    @property
    def value(self):
        return self.gmail.value

    @value.setter
    def value(self, value):
        self.gmail.value = value


class SettingCredentialsPath(ft.UserControl):
    def __init__(self, credentials_path, on_click):
        """設定タブの認証情報欄のためのコンポーネント

        Parameters
        ----------
        credentials_path : str
            認証情報が記述されているファイルのパス
        on_click
            コンポーネントのボタンをクリックした時実行する関数
        """
        super().__init__()
        self.selected_files = ft.Text(value=credentials_path)
        self.pick_files_dialog = ft.FilePicker(on_result=on_click)

    def build(self):
        return ft.Column(
            [
                ft.ElevatedButton(
                    "認証ファイルを選択",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: self.pick_files_dialog.pick_files(),
                ),
                self.selected_files,
            ]
        )

    @property
    def value(self):
        return self.selected_files.value

    @value.setter
    def value(self, value):
        self.selected_files.value = value


class SettingTab(ft.UserControl):
    def __init__(self, setting_list: list, add_settings):
        """設定タブコンポーネント

        Parameters
        ----------
        setting_list : list
            設定タブに表示するコンポーネントのリスト
        add_settings
            設定を適用する時用の関数
        """
        super().__init__()
        self.setting_list = setting_list
        self.add_settings = add_settings

    def build(self):
        return ft.Column(
            [
                *self.setting_list,
                ft.ElevatedButton("登録", on_click=self.add_settings),
            ]
        )


class Timetable(ft.UserControl):
    def __init__(self, open_dlg_modal):
        super().__init__()
        self.open_dlg = open_dlg_modal

    def open_dlg_modal(self, e):
        self.dlg_modal = InputModal()
        self.dlg_modal.column = e.control.content.controls
        self.dlg_modal.alert.open = True
        self.open_dlg()

    def build(self):
        def on_hover(e):
            e.control.bgcolor = "blue" if e.data == "true" else ft.colors.BLACK26
            e.control.update()

        timetable = []
        timetable.append(ft.Row([Card(ft.Text(week)) for week in ["", *WEEKS]]))

        for i in range(5):
            rows = []
            rows.append(Card(ft.Text(f"{i+1}限")))
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
            timetable.append(ft.Row(rows))
        return ft.Column(controls=timetable)


class Card(ft.UserControl):
    def __init__(self, content, on_click=None, on_hover=None):
        super().__init__()
        self.card = ft.Container(
            content=content,
            alignment=ft.alignment.center,
            width=100,
            height=100,
            bgcolor=ft.colors.BLACK26,
            border_radius=ft.border_radius.all(5),
            on_click=on_click,
            on_hover=on_hover,
        )

    def build(self):
        return self.card


class InputModal(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.column = []
        self.alert = ft.AlertDialog(
            modal=True,
            title=ft.Text("Please confirm"),
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def close_dlg(self, e):
        self.alert.open = False
        self.alert.update()

    def on_keyboard(self, e: ft.KeyboardEvent):
        if e.key == "Enter":
            self.register(e)
        if e.key == "Escape":
            self.close_dlg(e)

    def register(self, e):
        self.column[1] = ft.Text(f"{self.lecture_title.value}\n{self.place.value}")
        schedules[self.col0] = [self.lecture_title.value, self.place.value]
        self.close_dlg(e)
        self.update()

    def build(self):
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
        self.alert.actions = [
            ft.TextButton("登録", on_click=self.register),
            ft.TextButton("キャンセル", on_click=self.close_dlg),
        ]
        return self.alert


class RegisterModal(ft.UserControl):
    def __init__(self, datepicker, gmail, credentials_path, open_dlg):
        super().__init__()
        self.datepicker = datepicker
        self.gmail = gmail
        self.credentials_path = credentials_path
        self.open_dlg = open_dlg
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Googleカレンダーに登録"),
            actions=[
                ft.TextButton("登録", on_click=self.register),
                ft.TextButton("キャンセル", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.dlg_modal.update()

    def register(self, e):
        google_register.register(
            schedules,
            self.datepicker.selected_date,
            self.gmail,
            self.credentials_path,
        )
        self.close_dlg(e)

    def build(self):
        return self.dlg_modal

    def open(self, e):
        self.dlg_modal.open = True
        self.open_dlg()
