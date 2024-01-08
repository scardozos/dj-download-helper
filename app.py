import tkinter as tk
import os

DOWNLOADS_PATH = 'C:\\Users\\Santi\\Downloads'

supported_audio_extensions = [
    ".mp3",
    ".aiff",
    ".flag",
    ".wav"
]

class Model:
    def __init__(self):
        pass

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        tk.Frame.__init__(self, parent,width=200)
        label = tk.Label(self, text="Main Page")
        label.pack(pady=10,padx=10)
        self.list_music_files()

    def list_music_files(self):
    
        self.frame = tk.Frame(master=self.parent, width=200)
        self.frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.filelist = os.listdir(DOWNLOADS_PATH)
        self.musiclist = [filename for filename in self.filelist if os.path.splitext(filename)[1] in supported_audio_extensions]
        print(self.musiclist)

        self.listbox = tk.Listbox(master=self.frame, width=100, height=40)
        for name in self.musiclist:
            self.listbox.insert(tk.END, name)

        self.listbox.pack(fill=tk.BOTH, side=tk.LEFT, padx=10,pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)

    def handle_get_selection(self, event):
        selected_indices = self.listbox.curselection()
        for index in selected_indices:
            file_path = DOWNLOADS_PATH + "\\" + self.listbox.get(index) 
            print(f"Selected item at index {index}: {file_path}")

class View:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Complex Application")

        self.mainpage = MainPage
        self.mainpage(parent=root,controller=controller)

class Controller:
    def __init__(self,root):
        self.root = root
        self.model = Model()
        self.view = View(root, self)



if __name__ == "__main__":

    root = tk.Tk()
    app = Controller(root)
    root.mainloop()