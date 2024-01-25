import tkinter as tk
from .root_page import Root
from .main_page import MainPageView
from .config_page import ConfigPageView
from .error_page import ErrorPageView

class View:
    def __init__(self):
        self.root = Root()
        self.frames = {}

        self._add_frame(MainPageView, "mainpage")
        self._add_frame(ConfigPageView, "configpage")
        self._add_frame(ErrorPageView, "errorpage")

    def _add_frame(self, Frame: tk.Frame, name:str):
        self.frames[name] = Frame(self.root)
    
    def switch(self, name):
        print("executing switch")
        print(self.frames)
        frame = self.frames[name]
        frame.tkraise()
    
    def start_mainloop(self):
        self.root.mainloop()
