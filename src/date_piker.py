import flet as ft
import datetime
from dateutil.relativedelta import relativedelta
import calendar
import itertools


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


def main(page: ft.Page):
    def btn_calender_clicked(e):
        card.visible = not card.visible
        page.update()

    def date_selected():
        tf_date.value = datepiker.selected_date.strftime("%Y/%m/%d")
        card.visible = False
        page.update()

    tf_date = ft.TextField()
    btn_calender = ft.IconButton(
        icon=ft.icons.CALENDAR_TODAY, on_click=btn_calender_clicked
    )
    datepiker = DatePiker(on_selected=date_selected)
    card = ft.Card(
        ft.Container(
            datepiker,
            margin=10,
            width=300,
        ),
        visible=True,
    )

    page.theme_mode = ft.ThemeMode.LIGHT
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        btn_calender,
                        tf_date,
                    ]
                ),
                card,
                ft.Text("↑日付をカレンダーで入力できる"),
            ]
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
