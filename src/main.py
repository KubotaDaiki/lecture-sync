import flet as ft
from component import *


def main(page: ft.Page):
    def btn_calender_clicked(e):
        card.visible = not card.visible
        page.update()

    def date_selected():
        tf_date.value = datepicker.selected_date.strftime("%Y/%m/%d")
        card.visible = False
        page.update()

    def set_client_storage(e):
        if page.client_storage:
            page.client_storage.set("gmail", setting_gmail.value)
            page.client_storage.set("credentials_path", setting_credentials_path.value)

    def get_client_storage(get_list):
        storage_data = {}
        if page.client_storage:
            for get_data in get_list:
                storage_data[get_data] = page.client_storage.get(get_data)
        else:
            for get_data in get_list:
                storage_data[get_data] = None
        return storage_data

    def open_dlg(dlg, on_keyboard=None):
        if on_keyboard is not None:
            page.on_keyboard_event = on_keyboard
        page.dialog = dlg
        page.update()

    tf_date = ft.TextField()
    btn_calender = ft.IconButton(
        icon=ft.icons.CALENDAR_TODAY, on_click=btn_calender_clicked
    )
    datepicker = DatePiker(on_selected=date_selected)
    card = ft.Card(
        ft.Container(
            datepicker,
            margin=10,
            width=300,
        ),
        visible=True,
    )
    calender_set = ft.Column(
        [
            ft.Text("予定開始日"),
            ft.Row(
                [
                    btn_calender,
                    tf_date,
                ]
            ),
            card,
        ]
    )

    storage_data = get_client_storage(["gmail", "credentials_path"])

    setting_gmail = SettingGmail(storage_data["gmail"])
    setting_credentials_path = SettingCredentialsPath(storage_data["credentials_path"])
    page.overlay.append(setting_credentials_path.pick_files_dialog)

    timetable = Timetable(open_dlg)

    register_modal = RegisterModal(
        datepicker,
        setting_gmail,
        setting_credentials_path,
        open_dlg,
    )
    page.overlay.append(register_modal)

    page.add(
        ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="予定入力",
                    content=ft.Column(
                        [
                            calender_set,
                            timetable,
                            ft.ElevatedButton(
                                "Googleカレンダーに登録", on_click=register_modal.open
                            ),
                        ],
                        scroll="AUTO",
                    ),
                ),
                ft.Tab(
                    text="設定",
                    icon=ft.icons.SETTINGS,
                    content=SettingTab(
                        [
                            setting_gmail,
                            setting_credentials_path,
                        ],
                        set_client_storage,
                    ),
                ),
            ],
            expand=1,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
