import customtkinter as tk

class MessageWindow(tk.CTkToplevel):
    def __init__(self, title: str, message: str):
        super().__init__()
        self.title(title)
        self.attributes("-topmost", True)
        self.geometry("300x150")
        tk.CTkLabel(self, text=message).pack(pady=20)
        tk.CTkButton(self, text="OK", command=self.destroy).pack(pady=10)