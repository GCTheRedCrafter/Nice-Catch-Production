import customtkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image
import os

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

        tk.CTkButton(self, text="Profilbild auswählen", command=self.select_image).pack(pady=10)

        tk.CTkButton(self, text="Registrieren", command=self.register_user).pack(pady=10)
    
    def select_image(self):
        """Öffnet Dateiauswahl NUR für PNG - mit Confirm Button"""
        file_path = filedialog.askopenfilename(
            title="Profilbild auswählen (PNG)",
            filetypes=[("PNG Bilder", "*.png")]
        )
        
        if file_path:
            try:
                # Bild laden und skalieren
                img = Image.open(file_path)
                img.thumbnail((200, 250), Image.Resampling.LANCZOS)
                
                # VORSCHAU-FENSTER
                preview = tk.CTkToplevel(self)  # ← Kind von Hauptfenster
                preview.title("Profilbild Vorschau")
                preview.attributes("-topmost", True)
                preview.geometry("320x400")
                preview.transient(self)
                
                # Vorschau-Bild
                profile_img_preview = tk.CTkImage(light_image=img, dark_image=img, size=(220, 280))
                tk.CTkLabel(preview, image=profile_img_preview, text="").pack(pady=20)

                # BUTTON FRAME
                btn_frame = tk.CTkFrame(preview)
                btn_frame.pack(pady=20, padx=20, fill="x")
                
                # ✅ CONFIRM BUTTON (JETZT DA!)
                tk.CTkButton(btn_frame, 
                            text="✅ Verwenden", 
                            command=lambda fp=file_path: [self.confirm_image(fp), preview.destroy()],
                            fg_color="#4CAF50",
                            height=40).pack(side="left", padx=10, fill="x", expand=True)
                
                # ❌ CANCEL
                tk.CTkButton(btn_frame, 
                            text="❌ Abbrechen", 
                            command=preview.destroy,
                            fg_color="#f44336",
                            height=40).pack(side="right", padx=10)
                
                self.selected_image_path = file_path
                
            except Exception as e:
                messagebox.showerror("Fehler", f"PNG konnte nicht geladen werden:\n{str(e)}")

    def confirm_image(self, file_path):
        """Bestätigt Bildauswahl"""
        filename = os.path.basename(file_path)
        self.image_label = tk.CTkLabel(self, text=f"✅ {filename} wird verwendet", 
                                    text_color="#4CAF50", font=tk.CTkFont(size=12))
        self.image_label.pack(pady=5)
        self.selected_image_path = file_path  # Für register_user()

    def register_user(self):
        """Registriert User + speichert BILD NACH ERFOLG"""
        try:
            # 1. User erstellen (OHNE Bild)
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
            
            # 2. User ZUERST speichern
            self.storage.add_user(user_obj)
            user_id = user_obj.id
            
            # 3. BILD NACH ERFOLG speichern
            if self.selected_image_path:
                if self.save_profile_image(self.selected_image_path, user_id):
                    messagebox.showinfo("Erfolg", f"Registrierung erfolgreich!\nBild gespeichert als profile_{user_id}.png")
                else:
                    messagebox.showwarning("Warnung", "Registrierung OK, aber Bild konnte nicht gespeichert werden.")
            else:
                messagebox.showinfo("Erfolg", "Registrierung erfolgreich! (kein Bild)")
                
            self.destroy()
            
        except ValueError as e:
            messagebox.showerror("Fehler", f"Ungültige Eingabe: {str(e)}")
        except Exception as e:
            messagebox.showerror("Fehler", f"Registrierung fehlgeschlagen:\n{str(e)}")

    def save_profile_image(self, file_path, user_id):
        """Speichert PNG NACH Registrierung"""
        try:
            os.makedirs("img", exist_ok=True)
            new_path = f"img/profile_{user_id}.png"
            
            img = Image.open(file_path)
            img.thumbnail((400, 500), Image.Resampling.LANCZOS)
            img.save(new_path, "PNG", quality=95)
            
            # Pfad zurück zum User (optional)
            self.storage.data["users"][-1]["profile_image"] = new_path
            self.storage.save()
            return True
        
        except Exception as e:
            messagebox.showerror("Fehler", f"Bildfehler:\n{str(e)}")
            return False
    
    

if __name__ == "__main__":
    app = LoginWindow()
    #app = NiceCatchApp(current_user_id=1)  # Direkt zum Hauptfenster mit User-ID 1
    app.mainloop()