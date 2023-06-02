import flet as ft

WEEKS = ["月", "火", "水", "木", "金", "土", "日"]
all_data = {}


def main(page: ft.Page):
    def register_google_calendar(e):
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        def register(e):
            print(all_data)
            close_dlg(e)

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Googleカレンダーに登録"),
            actions=[
                ft.TextButton("登録", on_click=register),
                ft.TextButton("キャンセル", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    page.scroll = ft.ScrollMode.AUTO
    page.add(
        ft.Column(controls=items(page)),
        ft.Row(
            [
                ft.ElevatedButton("Googleカレンダーに登録", on_click=register_google_calendar),
                # ft.ElevatedButton("全削除", on_click=all_clear, color=ft.colors.RED),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


def all_clear(e):
    global all_data
    all_data = {}


def on_hover(e):
    e.control.bgcolor = "blue" if e.data == "true" else ft.colors.BLACK26
    e.control.update()


def items(page: ft.Page):
    def open_dlg_modal(e):
        dlg_modal = create_dlg_modal(page, e.control.content.controls)
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    all = []
    all.append(ft.Row([create_card(ft.Text(week)) for week in ["", *WEEKS]]))
    for i in range(5):
        rows = []
        rows.append(create_card(ft.Text(f"{i+1}限")))
        for j in range(7):
            item = create_card(
                ft.Column(
                    [
                        ft.Text(f"{j}{i}", visible=False),
                        ft.Text(f"{j}{i}", visible=False),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=open_dlg_modal,
                on_hover=on_hover,
            )
            rows.append(item)
        all.append(ft.Row(rows))
    return all


def create_card(content, on_click=None, on_hover=None):
    return ft.Container(
        content=content,
        alignment=ft.alignment.center,
        width=100,
        height=100,
        bgcolor=ft.colors.BLACK26,
        border_radius=ft.border_radius.all(5),
        on_click=on_click,
        on_hover=on_hover,
    )


def create_dlg_modal(page: ft.Page, col):
    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    def register(e):
        col[1] = ft.Text(f"{lecture_title.value}\n{place.value}")
        all_data[col0] = [lecture_title.value, place.value]
        close_dlg(e)

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Enter":
            register(e)
        if e.key == "Escape":
            close_dlg(e)

    col0 = col[0].value
    lecture_title = ft.TextField(label="講義名", autofocus=True)
    place = ft.TextField(label="場所")
    tmp = ft.Column(
        [
            ft.Text(f"{WEEKS[int(col0[0])]}曜{int(col0[1])+1}限", size=20),
            lecture_title,
            place,
        ]
    )
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Container(
            content=tmp,
            alignment=ft.alignment.center,
            width=500,
            height=500,
        ),
        actions=[
            ft.TextButton("登録", on_click=register),
            ft.TextButton("キャンセル", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.on_keyboard_event = on_keyboard
    return dlg_modal


ft.app(target=main)
