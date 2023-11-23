import flet as ft
from .Button import Button


class DatePickButton(ft.UserControl):
    def __init__(self, text, get_date):
        super().__init__()
        self.text = text

        self.date_picker = ft.DatePicker(
            on_change=get_date,
            on_dismiss=get_date,
            date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY,
        )

    def did_mount(self):
        if self.page is None:
            return

        self.page.overlay.append(self.date_picker)
        self.page.update()

    def build(self):
        return Button(
            text=self.text,
            icon="calendar_month",
            on_click=lambda _: self.date_picker.pick_date(),
            theme="light",
        )

    @property
    def value(self):
        if self.date_picker.value is None:
            return
        return self.date_picker.value.date()
