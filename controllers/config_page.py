import tkinter as tk
from common import config
from tkinter import ttk

class ConfigPageController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["configpage"]
        self.config: config.Config = self.model.config.config

        print(self.view)

        self.frame.button_close.config(command=self.go_to_mainpage)

    def go_to_mainpage(self):
        self.view.switch("mainpage")
        return 