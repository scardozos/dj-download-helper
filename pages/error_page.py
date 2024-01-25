import tkinter as tk

class ErrorPageView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        tk.Frame.__init__(self,width=100, height=40)
        self.grid(row=0,column=0, sticky=tk.NSEW, padx=10, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.err_msg_var = tk.StringVar()
        self.error_label = tk.Label(
            self,
            textvariable=self.err_msg_var,
            fg="red",
            font=("Helvetica", 16),
        )

        self.error_label.grid(
            column=0, 
            row=0, 
            sticky="nsew",
            pady=10,
            padx=10,
        )
