import os
import shutil
import tkinter as tk
from config import constants
from datetime import datetime
from config.enums import ListMode,MoveMode,MusicGenres, MusicCategory


class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.config = controller.config

        filelist = os.listdir(self.config.downloads_path)
        self.existing_musiclist = [filename for filename in filelist if os.path.splitext(filename)[1] in constants.SUPPORTED_AUDIO_EXTENSIONS]
        self.existing_musiclist.sort(key=lambda filename: os.path.getctime(os.path.join(self.config.downloads_path, filename)))

        # Init vars
        self.SELECTED_GENRE = self.config.default.music_genre.value
        self.SELECTED_CATEGORY = self.config.default.music_category.value
        self.SELECTED_FILE_PATH = ""
        self.SELECTED_FILE_NAME = ""

        self.CURRENT_COPY_MOVE_MODE = MoveMode.COPY.value
        self.REFRESH_MUSIC_LIST_ENABLED = False if (
            self.config.default.list_mode == ListMode.FULL_LIST_MODE
        ) else True
        self.CURRENT_LIST_MODE = self.config.default.list_mode 

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

        self.right_side_frame.grid_rowconfigure(0, weight=1)
        self.right_side_frame.grid_rowconfigure(1, weight=1)
        self.right_side_frame.grid_rowconfigure(2, weight=1)
        self.right_side_frame.grid_rowconfigure(3, weight=1)
        self.right_side_frame.grid_columnconfigure(0, weight=1)
        self.right_side_frame.grid_columnconfigure(1, weight=1)

        # Switch list mode button
        self.switch_list_mode_btn_txt = tk.StringVar(
            value=constants.SHOW_NEW_DOWNLOADS_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.SHOW_ALL_DOWNLOADS_TXT
        )

        self.switch_list_mode_btn = tk.Button(self.right_side_frame, textvariable=self.switch_list_mode_btn_txt, command=self.change_list_mode)
        self.switch_list_mode_btn.grid(column=0,row=0, sticky="nsew")

        # Switch refresh mode button
        self.switch_refresh_mode_btn_txt = tk.StringVar(
            value=constants.ENABLE_REFRESH_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.DISABLE_REFRESH_TXT
        )

        self.switch_refresh_mode_btn = tk.Button(self.right_side_frame, textvariable=self.switch_refresh_mode_btn_txt, command=self.change_automatic_refresh)
        self.switch_refresh_mode_btn.grid(column=1,row=0, sticky="nsew")
        
        # Music genres menubutton
        self.selected_genre_var = tk.StringVar(value=self.SELECTED_GENRE)
        self.selected_genre_var.trace_add("write", self.genres_menu_item_selected)

        self.genres_menu_btn = tk.Menubutton(self.right_side_frame, textvariable=self.selected_genre_var, relief=tk.RAISED)
        self.genres_menu = tk.Menu(self.genres_menu_btn, tearoff=0)

        for genre in self.config.displayed_music_genres:
            self.genres_menu.add_radiobutton(label=genre.value, variable=self.selected_genre_var)

        self.genres_menu_btn["menu"] = self.genres_menu
        self.genres_menu_btn.grid(row=1,column=0)


        # Music category menubutton
        self.selected_category_var = tk.StringVar(value=self.SELECTED_CATEGORY)
        self.selected_category_var.trace_add("write", self.categories_menu_item_selected)

        self.categories_menu_btn = tk.Menubutton(self.right_side_frame, textvariable=self.selected_category_var, relief=tk.RAISED)
        self.categories_menu = tk.Menu(self.categories_menu_btn, tearoff=0)

        for category in self.config.displayed_music_categories:
            self.categories_menu.add_radiobutton(label=category.value, variable=self.selected_category_var)

        self.categories_menu_btn["menu"] = self.categories_menu
        self.categories_menu_btn.grid(row=1,column=1)

        # Copy / MOVE menubutton

        self.selected_copy_move_var = tk.StringVar(value=self.CURRENT_COPY_MOVE_MODE)
        self.selected_copy_move_var.trace_add("write", self.copy_move_item_selected)

        self.copy_move_menu_btn = tk.Menubutton(self.right_side_frame, textvariable=self.selected_copy_move_var, relief=tk.SUNKEN)
        self.copy_move_menu = tk.Menu(self.copy_move_menu_btn, tearoff=0)

        for move_mode in [MoveMode.COPY, MoveMode.MOVE]:
            self.copy_move_menu.add_radiobutton(label=move_mode.value, variable=self.selected_copy_move_var, value=move_mode.value)

        self.copy_move_menu_btn["menu"] = self.copy_move_menu
        self.copy_move_menu_btn.grid(row=2, column=0)

        # Result frame
        self.res_frame = tk.Frame(self.right_side_frame, background="green")
        self.res_frame.grid(row=3, column=0, sticky="nsew", columnspan=2)

        # Resulting path label
        self.res_path_label_var = tk.StringVar(value=self.generate_move_path())
        self.res_path_label = tk.Label(self.res_frame, textvariable=self.res_path_label_var)
        self.move_btn = tk.Button(self.res_frame, text="Move", command=self.handle_copy_move)        
        
        self.move_res_label_var = tk.StringVar(value="")
        self.move_res_label = tk.Label(self.res_frame, textvariable=self.move_res_label_var)

        self.move_btn.grid(row=0, column=1, padx=5, pady=5)
        self.res_path_label.grid(row=0, column=0, padx=5, pady=5)
        self.move_res_label.grid(row=1,column=0, padx=5, pady=5)

    def handle_copy_move(self):
        to_directory = self.generate_move_path(dir_only=True)
        from_and_to_paths = [self.SELECTED_FILE_PATH, self.generate_move_path()]
        try:
            if not os.path.exists(to_directory):
                print(f"Creating directory '{to_directory}' as it doesn't exist yet")
                os.makedirs(to_directory)

            if self.CURRENT_COPY_MOVE_MODE == MoveMode.COPY.value:
                shutil.copy(*from_and_to_paths)
                restext = f"File '{self.SELECTED_FILE_NAME}' copied successfully"
                print(f"File copied successfully from '{from_and_to_paths[0]}' to '{from_and_to_paths[1]}'")
                self.move_res_label_var.set(restext)
            
            if self.CURRENT_COPY_MOVE_MODE == MoveMode.MOVE.value:
                shutil.move(*from_and_to_paths)
                restext = f"File '{self.SELECTED_FILE_NAME}' moved successfully"
                print(f"File moved successfully from '{from_and_to_paths[0]}' to '{from_and_to_paths[1]}'")
                self.move_res_label_var.set(restext)
        
        except FileNotFoundError as e:
            print(f"Error: {e}. The source file '{from_and_to_paths[0]}' does not exist")

        except Exception as e:
            print(f"Error moving file: {e}")
        pass

    def generate_move_path(self, dir_only=False) -> str:
        current_date = datetime.now()
        year_month_formatted = current_date.strftime("%m-%Y")

        path_list = [self.config.music_path,
                    f"{year_month_formatted} {self.SELECTED_GENRE} {self.SELECTED_CATEGORY}"]

        return (
            os.path.join(*path_list, self.SELECTED_FILE_NAME) 
            if (not dir_only)
            else os.path.join(*path_list)
        )
     
    def update_res_lbl(self):
        self.res_path_label_var.set(
            value=self.generate_move_path()
        )

    def copy_move_item_selected(self, var, index, mode):
        self.CURRENT_COPY_MOVE_MODE = self.selected_copy_move_var.get()
        print(f"Changed current move mode to {self.CURRENT_COPY_MOVE_MODE}")

    def genres_menu_item_selected(self, var, index, mode):
        self.SELECTED_GENRE = self.selected_genre_var.get()
        self.update_res_lbl()
        print(f"Selected genre {self.SELECTED_GENRE}")

    def categories_menu_item_selected(self, var, index, mode):
        self.SELECTED_CATEGORY = self.selected_category_var.get()
        self.update_res_lbl()
        print(f"Selected category {self.SELECTED_CATEGORY}")

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
        for name in self.existing_musiclist:
            self.listbox.insert(tk.END, name)

        self.listbox.yview(tk.END) if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE else None
        self.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)

    def update_file_list(self):
        print("calling update_file_list")
    
        self.filelist = os.listdir(self.config.downloads_path)

        self.current_musiclist = [filename for filename in self.filelist 
                                if os.path.splitext(filename)[1] in constants.SUPPORTED_AUDIO_EXTENSIONS
                                    if filename not in self.existing_musiclist]
        # print(self.musiclist)
        self.current_musiclist.sort(key=lambda filename: os.path.getctime(os.path.join(self.config.downloads_path, filename)))


        for name in self.current_musiclist:
            self.listbox.insert(tk.END, name)
            self.existing_musiclist.append(name)

        self.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)
        self.listbox.yview(tk.END) if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE else None

        if self.REFRESH_MUSIC_LIST_ENABLED:
            self.after(1000, self.update_file_list)


    def handle_get_selection(self, event):
        print("getting executed")
        selected_indices = self.listbox.curselection()
        for index in selected_indices:
            self.SELECTED_FILE_PATH = os.path.join(self.config.downloads_path,self.listbox.get(index)) 
            self.SELECTED_FILE_NAME = self.listbox.get(index)
            print(f"Selected item at index {index}: {self.SELECTED_FILE_PATH} - FILENAME: {self.SELECTED_FILE_NAME}")
        self.update_res_lbl()