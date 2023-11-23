import flet as ft


class Card(ft.UserControl):
    def __init__(self, content):
        super().__init__()
        self.content = content

    def build(self):
        self.card = ft.Container(
            content=self.content,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.BLUE_400,
            border_radius=ft.border_radius.all(5),
            border=ft.border.all(1, ft.colors.BLUE_300),
        )
        return self.card


class CardAction(ft.UserControl):
    def __init__(self, content, on_click, label=None):
        super().__init__()
        self.label = label
        self.card = ft.Container(
            content=content,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.WHITE,
            border_radius=ft.border_radius.all(5),
            on_click=lambda e: on_click(self),
            on_hover=self.on_hover,
            border=ft.border.all(1, ft.colors.BLUE_300),
        )

    def on_hover(self, e):
        e.control.bgcolor = ft.colors.BLUE if e.data == "true" else ft.colors.WHITE
        e.control.update()

    def build(self):
        return self.card
