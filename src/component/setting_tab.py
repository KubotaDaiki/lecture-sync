import flet as ft


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
    def __init__(self, credentials_path):
        """設定タブの認証情報欄のためのコンポーネント

        Parameters
        ----------
        credentials_path : str
            認証情報が記述されているファイルのパス
        on_click
            コンポーネントのボタンをクリックした時実行する関数
        """
        super().__init__()
        self.selected_files = ft.TextField(label="認証情報", value=credentials_path)
        self.file_dialog = ft.FilePicker(on_result=self.pick_files_result)

    def build(self):
        return ft.Column(
            [
                self.selected_files,
                ft.ElevatedButton(
                    "認証ファイルを選択",
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


class SettingTab(ft.UserControl):
    def __init__(self, setting_list: list, names: list, client_storage: ft.Page):
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
        self.names = names
        self.client_storage = client_storage

    def set_storage(self, e):
        if self.client_storage is not None:
            for name, setting in zip(self.names, self.setting_list):
                self.client_storage.set(name, setting.value)

    def add_setting(self, e):
        self.button.text = "登録しました"
        self.button.icon = "check"
        self.update()
        self.set_storage(e)

    def default(self, e):
        if e.data:
            self.button.text = "情報を登録"
            self.button.icon = "save"
            self.update()

    def build(self):
        self.button = ft.ElevatedButton(
            "情報を登録",
            icon="save",
            on_click=self.add_setting,
            on_hover=self.default,
            height=50,
            width=200,
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
        )
        return ft.Column(
            [
                *[
                    ft.Container(setting, margin=ft.margin.only(bottom=30))
                    for setting in self.setting_list
                ],
                self.button,
            ]
        )
