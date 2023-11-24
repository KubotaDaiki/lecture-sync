from turtle import width
import flet as ft


class Modal(ft.UserControl):
    def __init__(self, contents, on_click, close_modal, title=None):
        super().__init__()
        self.contents = contents
        self.on_click = on_click
        self.title_text = title
        self.close_modal = close_modal

    def _on_click(self, e):
        self.on_click()
        self.close_modal(e)

    def build(self):
        self.alert = ft.AlertDialog(
            content=ft.Container(
                ft.Column(self.contents, tight=True),
                margin=ft.margin.only(10, 10, 10, 50),
                width=400,
            ),
            modal=True,
            title=ft.Text(self.title_text),
            actions_alignment=ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("Cancel", on_click=self.close_modal),
                ft.TextButton("OK", on_click=self._on_click),
            ],
        )
        return self.alert

    @property
    def title(self):
        if self.alert.title is None:
            return
        return self.alert.title.value

    @title.setter
    def title(self, value):
        if self.alert.title is None:
            return
        self.alert.title.value = value

    @property
    def open(self):
        return self.alert.open

    @open.setter
    def open(self, value):
        self.alert.open = value
