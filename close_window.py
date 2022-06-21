from tkinter import *
from tkinter import messagebox
from child_window import Child_window
from window import Window


class Close_window:
    def __init__(self):
        pass

    def exit(self, this_window=Child_window, main_window=Window, question=str):
        if messagebox.askokcancel("Закрытие окна", question):
            this_window.root.destroy()
            main_window.root.destroy()

    def simple_close_window(self, this_window=Child_window):
        this_window.root.destroy()
