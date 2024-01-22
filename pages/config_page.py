import tkinter as tk
from tkinter import ttk
from common import config, constants

class ConfigPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.config : config.Config = controller.config

        tk.Frame.__init__(self, parent)

        button_close = ttk.Button(
            self,
            text="Close Window",
            command=self.destroy
        )

        button_close.grid(row=0,column=0, sticky="ew")