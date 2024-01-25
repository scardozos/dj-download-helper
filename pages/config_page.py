import tkinter as tk
from tkinter import ttk
from common import config, constants

class ConfigPageView(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Frame.__init__(self,width=100, height=40, background="blue")
        self.grid(row=0,column=0, sticky=tk.NSEW, padx=10, pady=10)

        self.button_close = ttk.Button(
            self,
            text="Close Window",
        )

        self.button_close.grid(row=0,column=0, sticky="ew")
