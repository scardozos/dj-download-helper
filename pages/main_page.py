import os
import tkinter as tk
from config import constants
from config.enums import ListMode


filelist = os.listdir(constants.DOWNLOADS_PATH)
existing_musiclist = [filename for filename in filelist if os.path.splitext(filename)[1] in constants.SUPPORTED_AUDIO_EXTENSIONS]
existing_musiclist.sort(key=lambda filename: os.path.getctime(os.path.join(constants.DOWNLOADS_PATH, filename)))

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller

        self.REFRESH_MUSIC_LIST_ENABLED = False
        self.CURRENT_LIST_MODE = controller.DEFAULT_LIST_MODE

        tk.Frame.__init__(self, parent,width=100, height=40, background="blue")

        self.grid(row=0,column=0, sticky=tk.NSEW, padx=10, pady=10)

        # Configure grid size
        self.grid_rowconfigure(0, weight=1)  
        self.grid_columnconfigure(0, weight=4) 
        self.grid_columnconfigure(1, weight=7)  

        # Show music listbox
        self.listbox = tk.Listbox(self, selectmode="single")
        self.listbox.grid(row=0, column=0, sticky=(tk.W,tk.N,tk.S, tk.E), padx=(0,5))


        # Show scrollbar
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.grid(row=0, column=0, sticky=(tk.N, tk.S,tk.E))

        # Link the Listbox with the Scrollbar
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.fill_file_list() if (
            self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE
        ) else self.update_file_list()
        
        # --- Start right side ---
        self.right_side_frame = tk.Frame(master=self, background="pink")
        self.right_side_frame.grid(row=0, column=1, sticky=(tk.E,tk.N,tk.S,tk.W))

        self.right_side_frame.grid_columnconfigure(0, weight=1)
        self.right_side_frame.grid_columnconfigure(1, weight=1)

        self.switch_list_mode_btn_txt = tk.StringVar(
            value=constants.SHOW_NEW_DOWNLOADS_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.SHOW_ALL_DOWNLOADS_TXT
        )

        self.switch_list_mode_btn = tk.Button(self.right_side_frame, textvariable=self.switch_list_mode_btn_txt, command=self.change_list_mode)
        self.switch_list_mode_btn.grid(column=0,row=0, sticky="nsew")

        self.switch_refresh_mode_btn_txt = tk.StringVar(
            value=constants.ENABLE_REFRESH_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.DISABLE_REFRESH_TXT
        )

        self.switch_refresh_mode_btn = tk.Button(self.right_side_frame, textvariable=self.switch_refresh_mode_btn_txt, command=self.change_automatic_refresh)
        self.switch_refresh_mode_btn.grid(column=1,row=0, sticky="nsew")

    def change_list_mode(self):
        print("calling change_list_mode")

        self.change_automatic_refresh() if (
            self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            and not self.REFRESH_MUSIC_LIST_ENABLED
        ) else None

        self.fill_file_list() if (
            self.CURRENT_LIST_MODE == ListMode.ONLY_NEW_MUSIC
        ) else None

        self.CURRENT_LIST_MODE = (
            ListMode.ONLY_NEW_MUSIC 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else ListMode.FULL_LIST_MODE
        )

        self.switch_list_mode_btn_txt.set(
            constants.SHOW_NEW_DOWNLOADS_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.SHOW_ALL_DOWNLOADS_TXT
        )

        self.listbox.delete(0, tk.END) if (
            self.CURRENT_LIST_MODE == ListMode.ONLY_NEW_MUSIC
        ) else None
        self.update_file_list()

    def change_automatic_refresh(self):
        print("calling change_automatic_refresh")

        self.REFRESH_MUSIC_LIST_ENABLED = (
            True if self.REFRESH_MUSIC_LIST_ENABLED is False else False
        )

        self.switch_refresh_mode_btn_txt.set(
            value=constants.ENABLE_REFRESH_TXT 
            if not self.REFRESH_MUSIC_LIST_ENABLED 
            else constants.DISABLE_REFRESH_TXT
        )

        self.update_file_list()
    
    def fill_file_list(self):
        for name in existing_musiclist:
            self.listbox.insert(tk.END, name)

    def update_file_list(self):
        print("calling update_file_list")
    
        self.filelist = os.listdir(constants.DOWNLOADS_PATH)

        self.current_musiclist = [filename for filename in self.filelist 
                                if os.path.splitext(filename)[1] in constants.SUPPORTED_AUDIO_EXTENSIONS
                                    if filename not in existing_musiclist]
        # print(self.musiclist)
        self.current_musiclist.sort(key=lambda filename: os.path.getctime(os.path.join(constants.DOWNLOADS_PATH, filename)))


        for name in self.current_musiclist:
            self.listbox.insert(tk.END, name)
            existing_musiclist.append(name)

        self.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)
        self.listbox.yview(tk.END) if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE else None

        if self.REFRESH_MUSIC_LIST_ENABLED:
            self.after(1000, self.update_file_list)


    def handle_get_selection(self, event):
        selected_indices = self.listbox.curselection()
        for index in selected_indices:
            file_path = os.path.join(constants.DOWNLOADS_PATH,self.listbox.get(index)) 
            print(f"Selected item at index {index}: {file_path}")