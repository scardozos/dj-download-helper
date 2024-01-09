import tkinter as tk
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

        self.file_list_frame = tk.Frame(master=self.parent, width=100)
        self.file_list_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.listbox = tk.Listbox(master=self.file_list_frame, width=100, height=40)
        self.listbox.pack(fill=tk.BOTH, side=tk.LEFT, padx=10,pady=10)

        self.update_file_list()
        self.right_side()

    def right_side(self):
        self.right_side_frame = tk.Frame(master=self.parent, width=800)
        self.right_side_frame.pack(fill=tk.BOTH, side=tk.LEFT)

    def update_file_list(self):
    
        #self.listbox.delete(0, tk.END)

        self.filelist = os.listdir(DOWNLOADS_PATH)
        
        self.current_musiclist = [filename for filename in self.filelist 
                                  if os.path.splitext(filename)[1] in supported_audio_extensions 
                                    if filename not in existing_musiclist]
        
        # print(self.musiclist)

        for name in self.current_musiclist:
            self.listbox.insert(tk.END, name)
            existing_musiclist.append(name)

        self.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)
        self.after(1000, self.update_file_list)

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