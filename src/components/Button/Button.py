import flet as ft


class Button(ft.UserControl):
    def __init__(self, text, icon=None, on_click=None, theme="blue"):
        super().__init__()
        self.text = text
        self.icon = icon
        self.on_click = on_click
        self.theme = theme

    def build(self):
        color = {
            "blue": {
                ft.MaterialState.DEFAULT: ft.colors.WHITE,
            },
            "light": None,
        }
        bgcolor = {
            "blue": {
                ft.MaterialState.DEFAULT: ft.colors.BLUE_700,
                ft.MaterialState.HOVERED: ft.colors.BLUE_900,
            },
            "light": None,
        }
        return ft.ElevatedButton(
            self.text,
            icon=self.icon,
            on_click=self.on_click,
            style=ft.ButtonStyle(
                padding={
                    ft.MaterialState.DEFAULT: ft.padding.symmetric(20, 30),
                },
                color=color[self.theme],
                bgcolor=bgcolor[self.theme],
                shape={
                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=15),
                },
            ),
        )
