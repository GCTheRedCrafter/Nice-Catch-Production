import tkinter as tk
from tkinter import messagebox
from modules.storage import Storage
from modules.logic import Matcher

class NiceCatchApp(tk.Tk):
    def __init__(self, current_user_id=1):
        super().__init__()
        self.title("NiceCatch")
        self.geometry("500x700")
        self.storage = Storage()
        self.matcher = Matcher(self.storage, current_user_id)
        self.current_profile = None

        self.build_widgets()
        self.load_next_profile()

    def build_widgets(self):
        self.card_frame = tk.Frame(self, bg="white")
        self.card_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.name_label = tk.Label(self.card_frame, font=("Arial", 20, "bold"))
        self.name_label.pack(pady=10)

        self.info_label = tk.Label(self.card_frame, font=("Arial", 12), justify="left")
        self.info_label.pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.dislike_btn = tk.Button(btn_frame, text="X", fg="red",
                                     command=self.skip_profile, width=10, height=2)
        self.dislike_btn.pack(side="left", padx=20)

        self.like_btn = tk.Button(btn_frame, text="Ball 🟡",
                                  command=self.like_profile, width=10, height=2)
        self.like_btn.pack(side="right", padx=20)

        self.more_btn = tk.Button(self, text="Für weitere Infos",
                                  command=self.show_details)
        self.more_btn.pack(pady=5)

    def load_next_profile(self):
        self.last_profile_id = self.current_profile["id"] if self.current_profile else None
        self.current_profile = self.matcher.get_next_profile(self.last_profile_id)
        if not self.current_profile:
            self.name_label.config(text="Keine weiteren Profile 😢")
            self.info_label.config(text="")
            return

        dog = self.current_profile["dog"]
        self.name_label.config(
            text=f'{dog["name"]} – {dog["age_years"]} Jahre, {dog["sex"]}'
        )
        self.info_label.config(
            text=f'Besitzer: {self.current_profile["name"]}, {self.current_profile["age"]} Jahre\n'
                 f'Ort: {self.current_profile["city"]}\n'
                 f'Interessen: {", ".join(self.current_profile["interests"])}'
        )

    def skip_profile(self):
        self.load_next_profile()

    def like_profile(self):
        if not self.current_profile:
            return
        chat_id = self.matcher.like_user(self.current_profile["id"])
        if chat_id is not None:
            messagebox.showinfo("Match!", f"Du hast ein Match! Chat-ID: {chat_id}")
        self.load_next_profile()

    def show_details(self):
        # hier könntest du ein neues Fenster mit mehr Infos öffnen
        if not self.current_profile:
            return
        messagebox.showinfo("Details", self.current_profile["bio"])

if __name__ == "__main__":
    app = NiceCatchApp()
    app.mainloop()