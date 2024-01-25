import os
import shutil
import tkinter as tk
from datetime import datetime
from common.enums import MoveMode, ListMode
from common import config, constants

class MainPageController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame = self.view.frames["mainpage"]

        if self.model.config.config is None:
            self.model.error.trigger("config is invalid")
            return

        self.config: config.Config = self.model.config.config

        filelist = os.listdir(self.config.downloads_path)
        self.existing_musiclist = [filename for filename in filelist if os.path.splitext(filename)[1] in constants.SUPPORTED_AUDIO_EXTENSIONS]
        self.existing_musiclist.sort(key=lambda filename: os.path.getctime(os.path.join(self.config.downloads_path, filename)))

        # Init vars
        self.SELECTED_GENRE = self.config.default.music_genre
        self.SELECTED_CATEGORY = self.config.default.music_category
        self.SELECTED_FILE_PATH = ""
        self.SELECTED_FILE_NAME = ""

        self.CURRENT_LIST_MODE = self.config.default.list_mode 
        self.CURRENT_COPY_MOVE_MODE = self.config.default.move_mode.value
        self.REFRESH_MUSIC_LIST_ENABLED = False if (
            self.config.default.list_mode == ListMode.FULL_LIST_MODE
        ) else True


        self.frame.switch_list_mode_btn_txt.set(
            constants.SHOW_NEW_DOWNLOADS_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.SHOW_ALL_DOWNLOADS_TXT
        )

        self.frame.switch_list_mode_btn.config(command=self.change_list_mode)

        self.frame.switch_refresh_mode_btn_txt.set(
            constants.ENABLE_REFRESH_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.DISABLE_REFRESH_TXT
        )

        self.frame.switch_refresh_mode_btn.config(command=self.change_automatic_refresh)

        self.frame.selected_genre_var.set(self.SELECTED_GENRE)
        self.frame.selected_genre_var.trace_add("write", self.genres_menu_item_selected)

        for genre in self.config.displayed_music_genres:
            self.frame.genres_menu.add_radiobutton(label=genre, variable=self.frame.selected_genre_var)

        self.frame.selected_category_var.set(self.SELECTED_CATEGORY)
        self.frame.selected_category_var.trace_add("write", self.categories_menu_item_selected)

        for category in self.config.displayed_music_categories:
            self.frame.categories_menu.add_radiobutton(label=category, variable=self.frame.selected_category_var)

        self.frame.selected_copy_move_var.set(self.CURRENT_COPY_MOVE_MODE)
        self.frame.selected_copy_move_var.trace_add("write", self.copy_move_item_selected)

        self.frame.res_path_label_var.set(self.generate_move_path())
        self.frame.move_btn.config(command=self.handle_copy_move)

        self._bind()

    def _bind(self):
        if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE:
            self.fill_file_list()
        else:
            self.update_file_list()

        pass

    def move_mode_state_listener(self, data):
        if data.current_move_mode == MoveMode.COPY:
            pass

    def fill_file_list(self):
        for name in self.existing_musiclist:
            self.frame.listbox.insert(tk.END, name)

        self.frame.listbox.yview(tk.END) if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE else None
        self.frame.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)

    def update_file_list(self):
        print("calling update_file_list")
    
        self.filelist = os.listdir(self.config.downloads_path)

        self.current_musiclist = [filename for filename in self.filelist 
                                if os.path.splitext(filename)[1] in constants.SUPPORTED_AUDIO_EXTENSIONS
                                    if filename not in self.existing_musiclist]
        # print(self.musiclist)
        self.current_musiclist.sort(key=lambda filename: os.path.getctime(os.path.join(self.config.downloads_path, filename)))


        for name in self.current_musiclist:
            self.frame.listbox.insert(tk.END, name)
            self.existing_musiclist.append(name)

        self.frame.listbox.bind("<<ListboxSelect>>", self.handle_get_selection)
        self.frame.listbox.yview(tk.END) if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE else None

        if self.REFRESH_MUSIC_LIST_ENABLED:
            self.frame.after(1000, self.update_file_list)

    def handle_get_selection(self, event):
        print("getting executed")
        selected_indices = self.frame.listbox.curselection()
        for index in selected_indices:
            self.SELECTED_FILE_PATH = os.path.join(self.config.downloads_path,self.frame.listbox.get(index)) 
            self.SELECTED_FILE_NAME = self.frame.listbox.get(index)
            print(f"Selected item at index {index}: {self.SELECTED_FILE_PATH} - FILENAME: {self.SELECTED_FILE_NAME}")
        self.update_res_lbl()

    def update_res_lbl(self):
        self.frame.res_path_label_var.set(
            self.generate_move_path()
        )

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

    def change_automatic_refresh(self):
        print("calling change_automatic_refresh")

        self.REFRESH_MUSIC_LIST_ENABLED = (
            True if self.REFRESH_MUSIC_LIST_ENABLED is False else False
        )

        self.frame.switch_refresh_mode_btn_txt.set(
            constants.ENABLE_REFRESH_TXT 
            if not self.REFRESH_MUSIC_LIST_ENABLED 
            else constants.DISABLE_REFRESH_TXT
        )

        self.update_file_list()
    
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

        self.frame.switch_list_mode_btn_txt.set(
            constants.SHOW_NEW_DOWNLOADS_TXT 
            if self.CURRENT_LIST_MODE == ListMode.FULL_LIST_MODE 
            else constants.SHOW_ALL_DOWNLOADS_TXT
        )

        self.frame.listbox.delete(0, tk.END) if (
            self.CURRENT_LIST_MODE == ListMode.ONLY_NEW_MUSIC
        ) else None

        self.update_file_list()

    def copy_move_item_selected(self, var, index, mode):
        self.CURRENT_COPY_MOVE_MODE = self.frame.selected_copy_move_var.get()
        print(f"Changed current move mode to {self.CURRENT_COPY_MOVE_MODE}")

    def genres_menu_item_selected(self, var, index, mode):
        self.SELECTED_GENRE = self.frame.selected_genre_var.get()
        self.update_res_lbl()
        print(f"Selected genre {self.SELECTED_GENRE}")

    def categories_menu_item_selected(self, var, index, mode):
        self.SELECTED_CATEGORY = self.frame.selected_category_var.get()
        self.update_res_lbl()
        print(f"Selected category {self.SELECTED_CATEGORY}")

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
                self.frame.move_res_label_var.set(restext)
            
            if self.CURRENT_COPY_MOVE_MODE == MoveMode.MOVE.value:
                shutil.move(*from_and_to_paths)
                restext = f"File '{self.SELECTED_FILE_NAME}' moved successfully"
                print(f"File moved successfully from '{from_and_to_paths[0]}' to '{from_and_to_paths[1]}'")
                self.frame.move_res_label_var.set(restext)
        
        except FileNotFoundError as e:
            print(f"Error: {e}. The source file '{from_and_to_paths[0]}' does not exist")

        except Exception as e:
            print(f"Error moving file: {e}")
        pass

     