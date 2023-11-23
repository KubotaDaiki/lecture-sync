import flet as ft


def get_client_storage(page: ft.Page, get_list: list):
    storage_data = {}
    if page.client_storage:
        for get_data in get_list:
            storage_data[get_data] = page.client_storage.get(get_data)
    else:
        for get_data in get_list:
            storage_data[get_data] = None
    return storage_data


def set_client_storage(page: ft.Page, set_dict):
    if page.client_storage is None:
        raise("client_storageがありません。")

    for key, value in set_dict.items():
        page.client_storage.set(key, value)
