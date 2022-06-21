from tkinter import *


class Window:
    def __init__(
        self,
        title,
        width,
        height,
        x=0,
        y=0,
        icon=None,
        resizable=(False, False),
    ):
        self.root = Tk()
        self.root.title(title)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(resizable[0], resizable[1])
        if icon is not None:
            self.root.iconbitmap(icon)

    def run(self):
        self.root.mainloop()
