from tkinter import *
from tkinter import messagebox
from child_window import Child_window
from window import Window


class Close_window:
    def __init__(self, main_win=Window):
        self.main_window = main_win

    def exit(self, this_window=Child_window, question=str):
        if messagebox.askokcancel("Закрытие окна", question):
            this_window.root.destroy()
            self.main_window.root.destroy()

    def simple_close_window(self, this_window=Child_window):
        this_window.root.destroy()

    def exit_account(self, profile=Child_window, client_area_window=Child_window):
        self.simple_close_window(profile)
        self.simple_close_window(client_area_window)
        self.main_window.root.deiconify()

    def close_window(self, this_window, title, question):
        if messagebox.askyesno(title, question):
            self.main_window.root.deiconify()
            this_window.root.destroy()
