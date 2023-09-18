import flet as ft
import component.main_tab as mt
import component.setting_tab as st


def main(page: ft.Page):
    # ページレイアウト
    page.title = "Lecture Sync"
    page.theme_mode = "light"
    page.window_maximized = True

    # ストレージデータの取得
    storage_data = get_client_storage(page, ["gmail", "credentials_path"])

    # 各部品の作成
    gmail = st.SettingGmail(storage_data["gmail"])

    credentials_path = st.SettingCredentialsPath(storage_data["credentials_path"])
    page.overlay.append(credentials_path.file_dialog)

    setting_tab = st.SettingTab(
        [
            gmail,
            credentials_path,
        ],
        ["gmail", "credentials_path"],
        page.client_storage,
    )

    calender = mt.Calendar(page.dialog)
    page.overlay.append(calender.modal)

    timetable = mt.Timetable(page.dialog, page.on_keyboard_event)
    page.overlay.append(timetable.modal.alert)

    registration_button = mt.RegistrationButton(
        calender.modal.datepicker,
        gmail,
        credentials_path,
        page.dialog,
    )
    page.overlay.append(registration_button.register)

    # 1つ目のタブを設定
    tab1 = ft.Tab(
        text="予定入力",
        content=ft.Column(
            [calender, timetable, registration_button],
            scroll="AUTO",
            horizontal_alignment="CENTER",
        ),
    )

    # 2つ目のタブを設定
    tab2 = ft.Tab(
        text="設定",
        icon=ft.icons.SETTINGS,
        content=ft.Container(
            setting_tab,
            margin=ft.margin.symmetric(vertical=40, horizontal=20),
        ),
    )

    # 各タブをpageに追加
    page.add(
        ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[tab1, tab2],
            expand=1,
        )
    )


def get_client_storage(page: ft.Page, get_list):
    storage_data = {}
    if page.client_storage:
        for get_data in get_list:
            storage_data[get_data] = page.client_storage.get(get_data)
    else:
        for get_data in get_list:
            storage_data[get_data] = None
    return storage_data


if __name__ == "__main__":
    ft.app(target=main)
