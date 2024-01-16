import tkinter as tk
from pages import main_page as mp
from config import coonfig

class Model:
    def __init__(self):
        pass

class View:
    def __init__(self, root, controller, window_width, window_height):
        self.root = root
        self.controller = controller
        self.root.title("DJ Music Download Helper")
        self.root.grid_rowconfigure(0, weight=1)  
        self.root.grid_columnconfigure(0, weight=1) 
        self.root.configure(background="dark gray")
        self.root.geometry(f"{window_width}x{window_height}")
        self.mainpage = mp.MainPage
        self.mainpage(parent=root,controller=controller)

class Controller:
    def __init__(self,root):
        self.root = root
        self.model = Model()
        self.config = coonfig.load_and_gen_if_not_exists()
        self.view = View(root, self, 1200, 600)


        print(self.config)

if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()