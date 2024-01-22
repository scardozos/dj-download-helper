import tkinter as tk

class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        window_width = 1200
        window_height = 600

        self.title("DJ Music Download Helper")
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=1) 
        self.configure(background="dark gray")
        self.geometry(f"{window_width}x{window_height}")