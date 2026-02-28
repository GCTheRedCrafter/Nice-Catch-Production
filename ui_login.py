import customtkinter as tk
from tkinter import messagebox
from PIL import Image

from modules.storage import Storage
from modules.logic import check_password
from modules.ui_main import NiceCatchApp
from modules.models import Dog, UserProfile
from modules.ui_utils import MessageWindow

class LoginWindow(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("NiceCatch Login")
        self.geometry("300x380")
        self.storage = Storage()
        self.build_widgets()

    def build_widgets(self):
        self.logo_image = tk.CTkImage(
            light_image=Image.open("img/logo.jpeg"),     # Pfad zu Bild
            dark_image=Image.open("img/logo.jpeg"),      # gleiches Bild oder anderes
            size=(100, 100)                         # Anzeigegröße (skaliert automatisch)
        )


        self.logo_label = tk.CTkLabel(self, image=self.logo_image, text="")
        self.logo_label.pack(pady=10)

        tk.CTkLabel(self, text="Benutzername:").pack(pady=5)
        self.username_entry = tk.CTkEntry(self)
        self.username_entry.pack(pady=5)

        tk.CTkLabel(self, text="Passwort:").pack(pady=5)
        self.password_entry = tk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.CTkButton(self, text="Login", command=self.attempt_login).pack(pady=10)

        tk.CTkButton(self, text="Registrieren", command=self.new_user).pack(pady=5)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = check_password(self.storage, username, password)
        if user_id:
            MessageWindow("Erfolg", f"Willkommen zurück, {username}!")
            self.destroy()  # Login-Fenster schließen
            # Hier könntest du das Hauptfenster starten und user_id übergeben
            NiceCatchApp(current_user_id=user_id).mainloop()
        else:
            MessageWindow("Fehler", "Ungültiger Benutzername oder Passwort.")
    
    def new_user(self):
        reg_window = RegisterWindow(self.storage)
        reg_window.mainloop()

class RegisterWindow(tk.CTkToplevel):
    def __init__(self, storage: Storage):
        super().__init__()
        self.title("Registrieren")
        self.attributes("-topmost", True)
        self.geometry("300x820")
        self.storage = storage
        self.build_widgets()

    def build_widgets(self):
        tk.CTkLabel(self, text="Benutzername:").pack(pady=5)
        self.username_entry = tk.CTkEntry(self)
        self.username_entry.pack(pady=5)

        tk.CTkLabel(self, text="Passwort:").pack(pady=5)
        self.password_entry = tk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=5)

        tk.CTkLabel(self, text="Alter:").pack(pady=5)
        self.age_entry = tk.CTkEntry(self)
        self.age_entry.pack(pady=5)

        tk.CTkLabel(self, text="Stadt:").pack(pady=5)
        self.city_entry = tk.CTkEntry(self)
        self.city_entry.pack(pady=5)

        tk.CTkLabel(self, text="Beschreibung:").pack(pady=5)
        self.bio_entry = tk.CTkEntry(self)
        self.bio_entry.pack(pady=5)

        tk.CTkLabel(self, text="Interessen (durch Kommata getrennt):").pack(pady=5)
        self.interests_entry = tk.CTkEntry(self)
        self.interests_entry.pack(pady=5)

        tk.CTkLabel(self, text="Name des Hundes:").pack(pady=5)
        self.dog_name_entry = tk.CTkEntry(self)
        self.dog_name_entry.pack(pady=5)

        tk.CTkLabel(self, text="Alter des Hundes:").pack(pady=5)
        self.dog_age_entry = tk.CTkEntry(self)
        self.dog_age_entry.pack(pady=5)

        tk.CTkLabel(self, text="Geschlecht des Hundes (Rüde/Hündin):").pack(pady=5)
        self.dog_sex_entry = tk.CTkEntry(self)
        self.dog_sex_entry.pack(pady=5)

        tk.CTkLabel(self, text="Beschreibung des Hundes:").pack(pady=5)
        self.dog_description_entry = tk.CTkEntry(self)
        self.dog_description_entry.pack(pady=5)

        tk.CTkButton(self, text="Registrieren", command=self.register_user).pack(pady=10)

    def register_user(self):
        # Hier würdest du die Eingaben validieren und einen neuen User anlegen
        dog_obj = Dog(
            id=len(self.storage.data["users"]) + 1,
            name=self.dog_name_entry.get(),
            age_years=int(self.dog_age_entry.get()),
            sex=self.dog_sex_entry.get(),
            description=self.dog_description_entry.get()
        )
        user_obj = UserProfile(
            id=len(self.storage.data["users"]) + 1,
            name=self.username_entry.get(),
            password=self.password_entry.get(),
            age=int(self.age_entry.get()),
            city=self.city_entry.get(),
            bio=self.bio_entry.get(),
            interests=[interest.strip() for interest in self.interests_entry.get().split(",")],
            dog=dog_obj
        )
        self.storage.add_user(user_obj)
        MessageWindow("Erfolg", "Registrierung erfolgreich! Du kannst dich jetzt einloggen.")
        self.destroy()

if __name__ == "__main__":
    #app = LoginWindow()
    app = NiceCatchApp(current_user_id=4)  # Direkt zum Hauptfenster mit User-ID 1
    app.mainloop()