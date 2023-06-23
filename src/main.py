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

    tf_date = ft.TextField(label="予定開始日", on_focus=btn_calender_clicked, width=300)
    datepicker = DatePiker(on_selected=date_selected)
    card = ft.Card(
        ft.Container(
            datepicker,
            margin=10,
            width=300,
        ),
        visible=False,
    )
    calender_set = ft.Column(
        [
            ft.Container(tf_date, margin=ft.margin.only(top=50, bottom=20)),
            card,
        ]
    )

    storage_data = get_client_storage(["gmail", "credentials_path"])

    setting_gmail = SettingGmail(storage_data["gmail"])
    setting_credentials_path = SettingCredentialsPath(storage_data["credentials_path"])
    page.overlay.append(setting_credentials_path.pick_files_dialog)
    setting_tab = SettingTab(
        [
            setting_gmail,
            setting_credentials_path,
        ],
        set_client_storage,
    )

    timetable = Timetable(open_dlg)

    register_modal = RegisterModal(
        datepicker,
        setting_gmail,
        setting_credentials_path,
        open_dlg,
    )
    page.overlay.append(register_modal)

    page.theme_mode = "light"
    page.window_maximized = True
    page.title = "Lecture Sync"

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
                            ft.Container(
                                ft.ElevatedButton(
                                    "Googleカレンダーに登録",
                                    height=50,
                                    width=300,
                                    icon="calendar_month",
                                    on_click=register_modal.open,
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
                                ),
                                margin=30,
                            ),
                        ],
                        scroll="AUTO",
                        horizontal_alignment="CENTER",
                    ),
                ),
                ft.Tab(
                    text="設定",
                    icon=ft.icons.SETTINGS,
                    content=ft.Container(
                        setting_tab,
                        margin=ft.margin.symmetric(vertical=40, horizontal=20),
                    ),
                ),
            ],
            expand=1,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
