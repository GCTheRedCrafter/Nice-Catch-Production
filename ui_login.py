import tkinter as tk
from tkinter import messagebox
from modules.storage import Storage
from modules.logic import check_password
from modules.ui_main import NiceCatchApp

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NiceCatch Login")
        self.geometry("300x200")
        self.storage = Storage()
        self.build_widgets()

    def build_widgets(self):
        tk.Label(self, text="Benutzername:").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Passwort:").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self, text="Login", command=self.attempt_login).pack(pady=10)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = check_password(self.storage, username, password)
        if user_id:
            messagebox.showinfo("Erfolg", f"Willkommen zurück, {username}!")
            self.destroy()  # Login-Fenster schließen
            # Hier könntest du das Hauptfenster starten und user_id übergeben
            main_app = NiceCatchApp(current_user_id=user_id)
            main_app.mainloop()
        else:
            messagebox.showerror("Fehler", "Ungültiger Benutzername oder Passwort.")

if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()