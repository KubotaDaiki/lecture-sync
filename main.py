import flet as ft


def main(page: ft.Page):
    weeks = ["", "月", "火", "水", "木", "金", "土", "日"]
    def on_hover(e):
        e.control.bgcolor = "blue" if e.data == "true" else ft.colors.BLACK26
        e.control.update()

    def items():
        all = []
        all.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(value=week),
                        alignment=ft.alignment.center,
                        width=100,
                        height=100,
                        bgcolor=ft.colors.BLACK26,
                        border_radius=ft.border_radius.all(5),
                    )
                    for week in weeks
                ]
            )
        )
        for i in range(5):
            rows = []
            rows.append(
                ft.Container(
                    content=ft.Text(value=f"{i+1}限"),
                    alignment=ft.alignment.center,
                    width=100,
                    height=100,
                    bgcolor=ft.colors.BLACK26,
                    border_radius=ft.border_radius.all(5),
                )
            )
            for j in range(7):
                item = ft.Container(
                    content=ft.Text(value=f"{weeks[j+1]}曜{i+1}限", visible=False),
                    alignment=ft.alignment.center,
                    width=100,
                    height=100,
                    bgcolor=ft.colors.BLACK26,
                    border_radius=ft.border_radius.all(5),
                    on_click=open_dlg_modal,
                    on_hover=on_hover,
                )
                rows.append(item)
            all.append(ft.Row(rows))
        return all

    def open_dlg_modal(e):
        dlg_modal = create_dlg_modal(e.control.content.value)
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def create_dlg_modal(value):
        def close_dlg(e):
            dlg_modal.open = False
            page.update()

        tmp = ft.Column(
            [
                ft.Text(f"{value}", size=20),
                ft.TextField(label="講義名"),
                ft.TextField(label="場所"),
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
                ft.TextButton("登録", on_click=close_dlg),
                ft.TextButton("キャンセル", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        return dlg_modal

    page.add(
        ft.Column(
            spacing=10,
            run_spacing=10,
            controls=items(),
        )
    )


ft.app(target=main)
