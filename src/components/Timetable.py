import flet as ft
from .Card import Card, CardAction


class Timetable(ft.UserControl):
    WEEKS = ["", "月", "火", "水", "木", "金", "土", "日"]

    def __init__(self, on_click):
        super().__init__()
        self.on_click = on_click

    def build(self):
        timetable = ft.GridView(runs_count=8)

        for week in self.WEEKS:
            timetable.controls.append(Card(ft.Text(week, color=ft.colors.WHITE)))

        for i in range(5):
            timetable.controls.append(Card(ft.Text(f"{i+1}限", color=ft.colors.WHITE)))
            for j in range(7):
                timetable.controls.append(
                    CardAction(
                        ft.Text(""),
                        on_click=self.on_click,
                        label=f"{i}{j}",
                    )
                )
        return ft.Container(
            content=timetable,
            width=1000,
        )
