from tkinter import *


class Child_window:
    def __init__(
        self,
        win_parent,
        title,
        width,
        height,
        x=0,
        y=0,
        icon=None,
        resizable=(False, False),
    ):
        self.root = Toplevel(win_parent)
        self.parent_win = win_parent
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(resizable[0], resizable[1])
        if icon is not None:
            self.root.iconbitmap(icon)

    def focus(self):
        self.root.grab_set()
        self.root.focus_set()
        self.root.wait_window()
