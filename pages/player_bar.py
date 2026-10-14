import tkinter as tk
from tkinter import ttk

class PlayerBar(ttk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grid_columnconfigure(4, weight=1)

        self.prev_btn = ttk.Button(self, text="⏮", width=3)
        self.play_pause_btn_txt = tk.StringVar(value="▶")
        self.play_pause_btn = ttk.Button(self, textvariable=self.play_pause_btn_txt, width=3)
        self.next_btn = ttk.Button(self, text="⏭", width=3)

        self.prev_btn.grid(row=0, column=0, rowspan=2, padx=(5, 0), pady=5)
        self.play_pause_btn.grid(row=0, column=1, rowspan=2, pady=5)
        self.next_btn.grid(row=0, column=2, rowspan=2, padx=(0, 5), pady=5)

        # Track name
        self.track_name_var = tk.StringVar(value="Nothing playing")
        self.track_name_label = ttk.Label(self, textvariable=self.track_name_var, anchor="w")
        self.track_name_label.grid(row=0, column=3, columnspan=3, sticky="ew", padx=5)

        # Seek slider
        self.time_elapsed_var = tk.StringVar(value="0:00")
        self.time_elapsed_label = ttk.Label(self, textvariable=self.time_elapsed_var, width=6, anchor="e")
        self.time_elapsed_label.grid(row=1, column=3, padx=(5, 0))

        self.seek_scale = ttk.Scale(self, orient=tk.HORIZONTAL, from_=0, to=0)
        self.seek_scale.grid(row=1, column=4, sticky="ew", padx=5, pady=(0, 5))

        self.time_total_var = tk.StringVar(value="0:00")
        self.time_total_label = ttk.Label(self, textvariable=self.time_total_var, width=6, anchor="w")
        self.time_total_label.grid(row=1, column=5, padx=(0, 5))
