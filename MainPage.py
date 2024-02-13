from threading import Thread
from tkinter import Tk, Frame

from views import MessageFrame


class MainPage:
    def __init__(self, master, user):
        self.message_page = None
        self.root = master
        self.root.geometry("400x600")
        self.root.title("autoMessage")
        self.page = self.create_page(user)

    def create_page(self, user):
        self.message_page = MessageFrame(self.root, user=user)
        self.message_page.pack()
        return self.message_page


if __name__ == '__main__':
    root = Tk()
    MainPage(master=root)
    root.mainloop()
