import tkinter as tk
from .root_page import Root
from .main_page import MainPageView

class View:
    def __init__(self):
        self.root = Root()
        self.frames = {}

        self._add_frame(MainPageView, "mainpage")

    def _add_frame(self, Frame: tk.Frame, name:str):
        self.frames[name] = Frame(self.root)
    
    def switch(self, name):
        frame = self.frames[name]
        frame.tkraise()
    
    def start_mainloop(self):
        self.root.mainloop()
