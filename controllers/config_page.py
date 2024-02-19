import tkinter as tk
from common import config
from common import helpers
from tkinter import ttk
from typing import List, Dict
from pages.config_page import ConfigPageView 
from tkinter import filedialog

class ConfigPageController():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.frame: ConfigPageView = self.view.frames["configpage"]
        self.config: config.Config = self.model.config.config

        self.error_model = self.model.error

        if self.config is None:
            self.error_model.trigger("Config not valid!")
            return

        # -- Downloads dir --

        self.frame.downloads_dir_btn.config(command=self.explore_downloads)
        
        self.add_to_entry(
            self.frame.downloads_dir_entry,
            self.config.downloads_path
        )

        # -- Music dir --

        self.frame.music_dir_btn.config(command=self.explore_music)
        self.add_to_entry(
            self.frame.music_dir_entry,
            self.config.music_path
        )

        # -- Spek dir --

        self.frame.spek_dir_btn.config(command=self.explore_spek)
        self.add_to_entry(
            self.frame.spek_dir_entry,
            self.config.spek_path
        )

        self.available_music_genres = self.config.available_music_genres
        self.displayed_music_genres = self.config.displayed_music_genres

        self.available_music_categories = self.config.available_music_categories
        self.displayed_music_categories = self.config.displayed_music_categories

        self.frame.button_close.config(command=self.go_to_mainpage)

        # -- Music Genres --
        self.fill_listbox_pair(
            available_config=self.frame.available_music_genres_listbox,
            available_values=self.available_music_genres,
            displayed_config=self.frame.displayed_music_genres_listbox,
            displayed_values=self.displayed_music_genres
        )

        # -- Music Categories -- 
        self.fill_listbox_pair(
            available_config=self.frame.available_music_categories_listbox,
            available_values=self.available_music_categories,
            displayed_config=self.frame.displayed_music_categories_listbox,
            displayed_values=self.displayed_music_categories
        )

        self.frame.add_genre_btn.config(command=self.handle_add_genres)
        self.frame.rm_genre_btn.config(command=self.handle_remove_genres)

        self.frame.add_category_btn.config(command=self.handle_add_categories)
        self.frame.rm_category_btn.config(command=self.handle_remove_categories)

    def get_all_configs(self):
        
        available_music_genres = self.get_listbox_config(
            self.frame.available_music_genres_listbox
        )
        displayed_music_genres = self.get_listbox_config(
            self.frame.displayed_music_genres_listbox
        )

        available_music_categories = self.get_listbox_config(
            self.frame.available_music_categories_listbox
        )
        displayed_music_categories = self.get_listbox_config(
            self.frame.displayed_music_categories_listbox
        )

        downloads_path = self.get_entry_config(
            self.frame.downloads_dir_entry
        )
        music_path = self.get_entry_config(
            self.frame.music_dir_entry
        )
        spek_path = self.get_entry_config(
            self.frame.spek_dir_entry
        )


        if self.error_model.err_happened == True:
            return

        self.new_config = config.Config(
            available_music_genres=available_music_genres,
            available_music_categories=available_music_categories,

            music_path=music_path,
            downloads_path=downloads_path,
            spek_path=spek_path,

            displayed_music_categories=displayed_music_categories,
            displayed_music_genres=displayed_music_genres,

            default=self.config.default
        )

        return self.new_config

    def explore_downloads(self):
        self.explore(
            self.frame.downloads_dir_entry,
        )

    def explore_music(self):
        self.explore(
            self.frame.music_dir_entry,
        )

    def explore_spek(self):
        self.explore(
            self.frame.spek_dir_entry
        )

    def explore(self, entry: tk.Entry):

        dir = filedialog.askdirectory()
        if dir:
            entry.delete(0, tk.END)
            entry.insert(0, dir)

    def fill_listbox_pair(
            self, 
            available_config: tk.Listbox, 
            displayed_config: tk.Listbox,
            available_values: List[str],
            displayed_values: List[str]
        ):
        self.fill_listbox_with_config(
            listbox=available_config,
            config_list=available_values
        )
        self.fill_listbox_with_config(
            listbox=displayed_config,
            config_list=displayed_values
        )

    def fill_listbox_with_config(self, listbox: tk.Listbox, config_list):
        for item in config_list:
            self.add_to_listbox(listbox, item)
        
    
    def handle_add_genres(self):
        selected_indices = self.frame.available_music_genres_listbox.curselection()
        print(selected_indices)
        for index in selected_indices:
            self.add_available_to_displayed(
                        idx=index,
                        available_listbox=self.frame.available_music_genres_listbox,
                        displayed_list=self.displayed_music_genres,
                        displayed_listbox=self.frame.displayed_music_genres_listbox
            )

    def handle_remove_genres(self):
        self.handle_remove_config(
            available_config_list=self.available_music_genres,
            available_config_listbox=self.frame.available_music_genres_listbox,
            displayed_config_list=self.displayed_music_genres,
            displayed_config_listbox=self.frame.displayed_music_genres_listbox
        )

    def handle_remove_categories(self):
        self.handle_remove_config(
            available_config_list=self.available_music_categories,
            available_config_listbox=self.frame.available_music_categories_listbox,
            displayed_config_list=self.displayed_music_categories,
            displayed_config_listbox=self.frame.displayed_music_categories_listbox
        )

    def handle_add_categories(self):
        selected_indices = self.frame.available_music_categories_listbox.curselection()
        print(selected_indices)
        for index in selected_indices:
            self.add_available_to_displayed(
                        idx=index,
                        available_listbox=self.frame.available_music_categories_listbox,
                        displayed_list=self.displayed_music_categories,
                        displayed_listbox=self.frame.displayed_music_categories_listbox
            )

    def get_listbox_config(
            self,
            listbox: tk.Listbox,
        ) -> List[str]:

        all_items = listbox.get(0, tk.END)

        return all_items

    def get_entry_config(
            self,
            entry: tk.Entry
    ) -> str:
        
        value = entry.get()

        if value == "":
            self.error_model.trigger(
                "Entry must not be empty!"
            ) 
            return

        if helpers.is_valid_path(value) == False:
            self.error_model.trigger(
                "Entry is not a valid path!"
            )
            return

        return value



    def handle_remove_config(
            self,
            displayed_config_listbox: tk.Listbox,
            available_config_listbox: tk.Listbox,
            available_config_list: List[str],
            displayed_config_list: List[str]
        ):
        selected_displayed_config = displayed_config_listbox.curselection()
        selected_available_config = available_config_listbox.curselection()

        selected_idx = -1

        if selected_available_config:
            selected_idx = selected_available_config[0]
            selected_list = available_config_list
            selected_listbox = available_config_listbox

        if selected_displayed_config:
            selected_idx = selected_displayed_config[0]
            selected_list = displayed_config_list
            selected_listbox = displayed_config_listbox 

        if selected_idx != -1:
            self.remove_from_displayed_or_available(
                idx=selected_idx,
                items_list=selected_list,
                items_listbox=selected_listbox
            )            

    def add_available_to_displayed(
            self, 
            idx: int,
            available_listbox: tk.Listbox, 
            displayed_listbox: tk.Listbox,
            displayed_list: List[str]
        ):
        
        selected_item = available_listbox.get(idx)
        print(f"selected item {selected_item}")

        if selected_item not in displayed_list:
            self.add_to_listbox(displayed_listbox, selected_item)
            displayed_list.append(selected_item)
        
    
    def remove_from_displayed_or_available(
            self,
            idx: int,
            items_listbox: tk.Listbox,
            items_list: List[str]
        ):
        
        selected_item = items_listbox.get(idx)
        print(f"selected item {selected_item}")

        if selected_item in items_list:
            self.rm_from_listbox(items_listbox, selected_item)
            items_list.remove(selected_item)

    def add_to_entry(self, entry: tk.Entry, item: str):
        entry.insert(0, item)
        return

    def add_to_listbox(self, listbox: tk.Listbox, item: str):
        listbox.insert(tk.END, item)
        return

    def rm_from_listbox(self, listbox: tk.Listbox, item: str):
        idx = listbox.get(0, tk.END).index(item)
        listbox.delete(idx)
        return

    def go_to_mainpage(self):
        new_config = self.get_all_configs()
        if self.error_model.err_happened:
            return
        self.model.config.save_new(new_config)
        self.view.switch("mainpage")
        return 