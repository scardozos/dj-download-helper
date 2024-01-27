import tkinter as tk
from tkinter import ttk
from common import config, constants

class ConfigPageView(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Frame.__init__(self,width=100, height=40, background="blue")

        self.grid(row=0,column=0, sticky=tk.NSEW, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.button_close = ttk.Button(
            self,
            text="Close Config Page",
        )

        self.button_close.grid(row=0,column=0, sticky="new")

        # --- left column ---

        self.lbl_padding = 10
        self.add_rm_btn_width = 10
        self.listbox_padding = 10

        self.lbl_params = {"width": 20}
        self.listbox_params = {"width": 20}
        self.add_btn_params = {"text":"ADD", "width":self.add_rm_btn_width}
        self.rm_btn_params = {"text":"REMOVE", "width":self.add_rm_btn_width}
        self.lbl_grid_params = {"sticky":"nsew", "padx":self.lbl_padding, "pady":self.lbl_padding}
        self.listbox_grid_params = {"rowspan":3, "sticky": "nsew", "pady": self.listbox_padding, "padx": self.listbox_padding}

        # -- available / displayed music genres config --

        self.genres_frame = tk.Frame(self) 
        self.genres_frame.grid(column=0, row=1, sticky="news", padx=10, pady=10)

        self.genres_frame.grid_rowconfigure(0, weight=0)
        self.genres_frame.grid_rowconfigure(1, weight=1)
        self.genres_frame.grid_rowconfigure(2, weight=1)

        self.genres_frame.grid_columnconfigure(0, weight=1)
        self.genres_frame.grid_columnconfigure(1, weight=0)
        self.genres_frame.grid_columnconfigure(2, weight=1)


        self.available_music_genres_label = tk.Label(self.genres_frame, text=constants.AVAILABLE_MUSIC_GENRES_TXT, **self.lbl_params)
        self.available_music_genres_listbox = tk.Listbox(self.genres_frame, selectmode="", **self.listbox_params)

        
        self.add_genre_btn = tk.Button(self.genres_frame, **self.add_btn_params)
        self.rm_genre_btn = tk.Button(self.genres_frame, **self.rm_btn_params)

        self.displayed_music_genres_label = tk.Label(self.genres_frame, text=constants.DISPLAYED_MUSIC_GENRES_TXT, **self.lbl_params)
        self.displayed_music_genres_listbox = tk.Listbox(self.genres_frame, selectmode="", **self.listbox_params)

        # available / displayed genres gridding
        self.available_music_genres_label.grid(column=0, row=0, **self.lbl_grid_params)
        self.available_music_genres_listbox.grid(column=0, row=1, **self.listbox_grid_params)

        self.add_genre_btn.grid(column=1, row=1)
        self.rm_genre_btn.grid(column=1, row=2)

        self.displayed_music_genres_label.grid(column=2, row=0, **self.lbl_grid_params)
        self.displayed_music_genres_listbox.grid(column=2, row=1, **self.listbox_grid_params)

        # -- available / displayed music categories config --

        self.categories_frame = tk.Frame(self) 
        self.categories_frame.grid(column=0, row=2, sticky="news", padx=10, pady=10)

        self.categories_frame.grid_rowconfigure(0, weight=0)
        self.categories_frame.grid_rowconfigure(1, weight=1)
        self.categories_frame.grid_rowconfigure(2, weight=1)

        self.categories_frame.grid_columnconfigure(0, weight=1)
        self.categories_frame.grid_columnconfigure(1, weight=0)
        self.categories_frame.grid_columnconfigure(2, weight=1)

        self.available_music_categories_label = tk.Label(self.categories_frame, text=constants.AVAILABLE_MUSIC_CATEGORIES_TXT, **self.lbl_params)
        self.available_music_categories_listbox = tk.Listbox(self.categories_frame, selectmode="", **self.listbox_params)

        
        self.add_category_btn = tk.Button(self.categories_frame, **self.add_btn_params)
        self.rm_category_btn = tk.Button(self.categories_frame, **self.rm_btn_params)

        self.displayed_music_categories_label = tk.Label(self.categories_frame, text=constants.DISPLAYED_MUSIC_CATEGORIES_TXT, **self.lbl_params)
        self.displayed_music_categories_listbox = tk.Listbox(self.categories_frame, selectmode="", **self.listbox_params)

        # available / displayed categories gridding
        self.available_music_categories_label.grid(column=0, row=0, **self.lbl_grid_params)
        self.available_music_categories_listbox.grid(column=0, row=1, **self.listbox_grid_params)

        self.add_category_btn.grid(column=1, row=1)
        self.rm_category_btn.grid(column=1, row=2)

        self.displayed_music_categories_label.grid(column=2, row=0, **self.lbl_grid_params)
        self.displayed_music_categories_listbox.grid(column=2, row=1, **self.listbox_grid_params)

        # --- right column ---


