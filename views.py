import tkinter as tk
from threading import Thread
from time import sleep
from tkinter import ttk
import platform
import requests
from pyperclip import copy
from win10toast import ToastNotifier
from win11toast import notify


def get_message(user):
    url = "http://127.0.0.1:8000/get_message/"
    data = {}
    key1 = "username"
    value1 = user
    print(user)
    data[key1] = value1
    res = requests.get(url, params=data)
    if res.text == "no message":
        return "", ""
    data = res.json()
    message = data["message"]
    date = data["date"]
    ret = (message, date)
    return ret


def update_message(message):
    # 获取代码运行环境
    version = ""
    os_platform = platform.system()
    if os_platform == "Windows":
        os_version = platform.version()
        version = os_version.split(".")
        version = version[2]
    elif os_platform == "Linux":
        pass
    elif os_platform == "Darwin":  # Mac OS
        pass
    if int(version) < 20000:  # Windows 10
        toaster = ToastNotifier()
        toaster.show_toast("新短信", message, duration=5, callback_on_click=copy_to_board(message))
    else:  # Windows 11
        if message != "no message":
            notify('新短信', message, duration='long', on_click=copy_to_board(message))


def copy_to_board(message):
    copy(message)
    return 1


class MessageFrame(tk.Frame):
    def __init__(self, root, user):
        super().__init__(root)
        self.tree_view = None
        self.table_view = tk.Frame()
        self.table_view.pack()
        tk.Label(self, text=user + ",你好").pack()
        self.create_page(user)

    def create_page(self, user):
        columns = ("message", "date")
        columns_values = ("消息", "日期")

        self.tree_view = ttk.Treeview(self, show="headings", columns=columns)
        self.tree_view.column('message', width=250, anchor="center")
        self.tree_view.column("date", width=150, anchor="center")
        self.tree_view.heading("message", text='消息')
        self.tree_view.heading("date", text='日期')
        self.tree_view.pack(fill=tk.BOTH, expand=True)
        self.show_data_frame(user)

    def show_data_frame(self, user):
        res = get_message(user)
        print(res)
        self.tree_view.insert("", "end", values=res)
        if res[0] != "":
            update_message(res[0])

    def in_show_data_frame(self, user):
        while True:
            sleep(2)
            res = get_message(user)
            print(res)
            self.tree_view.insert("", "end", values=res)
            if res[0] != "":
                update_message(res[0])