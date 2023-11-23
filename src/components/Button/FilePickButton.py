import flet as ft


class FilePickButton(ft.UserControl):
    def __init__(self, field_label, button_text, value):
        super().__init__()
        self.selected_files = ft.TextField(label=field_label, value=value)
        self.file_dialog = ft.FilePicker(on_result=self.pick_files_result)
        self.button_text = button_text

    def build(self):
        return ft.Column(
            [
                self.selected_files,
                ft.ElevatedButton(
                    self.button_text,
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=lambda _: self.file_dialog.pick_files(),
                    height=40,
                    elevation=3,
                ),
            ]
        )

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        if not e.files:
            return
        self.value = e.files[0].path
        self.update()

    @property
    def value(self):
        return self.selected_files.value

    @value.setter
    def value(self, value):
        self.selected_files.value = value
