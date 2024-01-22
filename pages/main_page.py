import tkinter as tk
from common.enums import MoveMode

class MainPageView(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        tk.Frame.__init__(self,width=100, height=40, background="blue")

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
            value=""
        )

        # Switch refresh mode button
        self.switch_refresh_mode_btn_txt = tk.StringVar(
            value=""
        )
        self.switch_list_mode_btn = tk.Button(self.right_side_frame, textvariable=self.switch_list_mode_btn_txt)
        self.switch_list_mode_btn.grid(column=0,row=0, sticky="nsew")


        self.switch_refresh_mode_btn = tk.Button(self.right_side_frame, textvariable=self.switch_refresh_mode_btn_txt)
        self.switch_refresh_mode_btn.grid(column=1,row=0, sticky="nsew")
        
        # Music genres menubutton
        self.selected_genre_var = tk.StringVar(value="")

        self.genres_menu_btn = tk.Menubutton(self.right_side_frame, textvariable=self.selected_genre_var, relief=tk.RAISED)
        self.genres_menu = tk.Menu(self.genres_menu_btn, tearoff=0)


        self.genres_menu_btn["menu"] = self.genres_menu
        self.genres_menu_btn.grid(row=1,column=0)

        # Music category menubutton
        self.selected_category_var = tk.StringVar(value="")

        self.categories_menu_btn = tk.Menubutton(self.right_side_frame, textvariable=self.selected_category_var, relief=tk.RAISED)
        self.categories_menu = tk.Menu(self.categories_menu_btn, tearoff=0)

        self.categories_menu_btn["menu"] = self.categories_menu
        self.categories_menu_btn.grid(row=1,column=1)

        # Copy / MOVE menubutton

        self.selected_copy_move_var = tk.StringVar(value="")

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
        self.res_path_label_var = tk.StringVar(value="")
        self.res_path_label = tk.Label(self.res_frame, textvariable=self.res_path_label_var)
        self.move_btn = tk.Button(self.res_frame, text="Move")        
        
        self.move_res_label_var = tk.StringVar(value="")
        self.move_res_label = tk.Label(self.res_frame, textvariable=self.move_res_label_var)

        self.move_btn.grid(row=0, column=1, padx=5, pady=5)
        self.res_path_label.grid(row=0, column=0, padx=5, pady=5)
        self.move_res_label.grid(row=1,column=0, padx=5, pady=5)
