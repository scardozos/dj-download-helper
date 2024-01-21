import tkinter as tk

class ErrorPage(tk.Frame):
    def __init__(self, root, controller, err_msg):
        self.root = root
        self.controller = controller

        self.error_label = tk.Label(
            self.root,
            text=err_msg,
            fg="red",
            font=("Helvetica", 16)
        )

        self.error_label.grid(
            column=0, 
            row=0, 
            sticky="nsew",
            pady=10,
            padx=10
        )
