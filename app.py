import platform
import tkinter as tk
from tkinter import ttk
from enum import Enum
import os

DOWNLOADS_PATH = 'C:\\Users\\Santi\\Downloads'

supported_audio_extensions = [
    ".mp3",
    ".aiff",
    ".flag",
    ".wav"
]

filelist = os.listdir(DOWNLOADS_PATH)
existing_musiclist = [filename for filename in filelist if os.path.splitext(filename)[1] in supported_audio_extensions]

class ListMode(Enum):
    FULL_LIST_MODE = "full_list_mode"
    ONLY_NEW_MUSIC = "only_new_music"

class Model:
    def __init__(self):
        pass

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        self.REFRESH_MUSIC_LIST_ENABLED = False
        self.DEFAULT_LIST_MODE = ListMode.FULL_LIST_MODE

        self.CURRENT_LIST_MODE = self.DEFAULT_LIST_MODE

        tk.Frame.__init__(self, parent,width=100, height=40, background="blue")

        self.grid(row=0,column=0, sticky=tk.NSEW, padx=10, pady=10)

        # Configure grid size
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=4) 
        self.grid_columnconfigure(1, weight=7)  

        # Show music listbox
        self.listbox = tk.Listbox(self)
        self.listbox.grid(row=0, column=0, sticky=(tk.W,tk.N,tk.S, tk.E), padx=(0,5))


        # Show scrollbar
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=0, column=0, sticky=(tk.N, tk.S,tk.E))

        # Link the Listbox with the Scrollbar
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.update_file_list()
        
        # --- Start right side ---
        self.right_side_frame = tk.Frame(master=self, background="pink")
        self.right_side_frame.grid(row=0, column=1, sticky=(tk.E,tk.N,tk.S,tk.W))

    def enable_automatic_refresh(self):
        self.REFRESH_MUSIC_LIST_ENABLED = True
        self.listbox.delete(0, tk.END)
        self.update_file_list()
    
    def disable_automatic_refresh(self):
        self.REFRESH_MUSIC_LIST_ENABLED = False
        self.listbox.delete(0, tk.END)
        self.update_file_list()

    def update_file_list(self):
    
        self.filelist = os.listdir(DOWNLOADS_PATH)
        

        self.current_musiclist = []

        if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE:
            self.current_musiclist = [filename for filename in self.filelist 
                                  if os.path.splitext(filename)[1] in supported_audio_extensions]
        
        if self.CURRENT_LIST_MODE == ListMode.ONLY_NEW_MUSIC:
            self.current_musiclist = [filename for filename in self.filelist 
                                    if os.path.splitext(filename)[1] in supported_audio_extensions 
                                        if filename not in existing_musiclist]
        # print(self.musiclist)
        self.current_musiclist.sort(key=lambda filename: os.path.getctime(os.path.join(DOWNLOADS_PATH, filename)))

        for name in self.current_musiclist:
            self.listbox.insert(tk.END, name)
            existing_musiclist.append(name)

        self.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)

        if self.REFRESH_MUSIC_LIST_ENABLED:
            self.after(1000, self.update_file_list)

        self.listbox.yview(tk.END) if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE else None


    def handle_get_selection(self, event):
        selected_indices = self.listbox.curselection()
        for index in selected_indices:

            file_path = os.path.join(DOWNLOADS_PATH,self.listbox.get(index)) 
            print(f"Selected item at index {index}: {file_path}")

class View:
    def __init__(self, root, controller, window_width, window_height):
        self.root = root
        self.controller = controller
        self.root.title("Download Helper")
        self.root.grid_rowconfigure(0, weight=1)  
        self.root.grid_columnconfigure(0, weight=1) 
        self.root.configure(background="dark gray")
        self.root.geometry(f"{window_width}x{window_height}")
        self.mainpage = MainPage
        self.mainpage(parent=root,controller=controller)

class Controller:
    def __init__(self,root):
        self.root = root
        self.model = Model()
        self.view = View(root, self, 1200, 600)


if __name__ == "__main__":
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()