import customtkinter as tk
from tkinter import filedialog
from PIL import Image
import os

from modules.ui_utils import MessageWindow
from modules.storage import Storage
from modules.logic import Matcher

class ProfileWindow(tk.CTkToplevel):
    def __init__(self, storage: Storage, current_user_id: int):
        super().__init__()
        self.storage = storage
        self.profile_data = self.storage.data["users"][current_user_id - 1]
        self.title(f"{self.profile_data['name']}'s Profil")
        self.attributes("-topmost", True)
        self.geometry("400x600")
        self.build_widgets()

    def build_widgets(self):

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.chat_btn = tk.CTkButton(self, text="Speichern", command=self.save)
        self.chat_btn.grid(row=0, column=2, sticky="ne", padx=(5, 10), pady=10)

        self.change_img_btn = tk.CTkButton(self, text="Profilbild ändern", 
            command=lambda: self.select_image())

        self.change_img_btn.grid(row=0, column=1, sticky="ne", padx=(150, 5), pady=10)

        self.title_label = tk.CTkLabel(self, text="NiceCatch", font=tk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="nw", padx=10, pady=10)
        
        self.card_frame = tk.CTkScrollableFrame(self, fg_color="#dddddd", corner_radius=15)
        self.card_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=15, pady=15)
        self.card_frame.grid_columnconfigure(0, weight=1)

        # PROFILBILD
        try:
            img_path = f"img/profile_{self.profile_data['id']}.png"
            profile_image = Image.open(img_path)
        except FileNotFoundError:
            try:
                profile_image = Image.open("img/logo.jpeg")
            except:
                profile_image = None

        if profile_image:
            profile_img = tk.CTkImage(light_image=profile_image, dark_image=profile_image, size=(350, 420))
            picture_label = tk.CTkLabel(self.card_frame, image=profile_img, text="")
            picture_label.pack(pady=20)
        else:
            picture_label = tk.CTkLabel(self.card_frame, text="🐕", font=tk.CTkFont(size=80))
            picture_label.pack(pady=20)

        # NAME
        self.dog_basics_frame = tk.CTkFrame(self.card_frame, fg_color="transparent")
        self.dog_basics_frame.pack(pady=0, padx=25, fill="x", expand=True)

        dog = self.profile_data["dog"]

        self.dog_name_entry = tk.CTkEntry(self.dog_basics_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray")
        self.dog_name_entry.insert(0, dog["name"])
        self.dog_name_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.dog_age_entry = tk.CTkEntry(self.dog_basics_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray", width=50)
        self.dog_age_entry.insert(0, dog["age_years"])
        self.dog_age_entry.pack(side="left", padx=5)

        self.dog_sex_entry = tk.CTkEntry(self.dog_basics_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray", width=50)
        self.dog_sex_entry.insert(0, dog["sex"])
        self.dog_sex_entry.pack(side="left", padx=(5, 0))

        self.dog_info_entry = tk.CTkEntry(self.card_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray")
        self.dog_info_entry.insert(0, dog["description"])
        self.dog_info_entry.pack(pady=(8, 0), padx=25, fill="x", expand=True)

        # INFO  
        self.owner_name_entry = tk.CTkEntry(self.card_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray")
        self.owner_name_entry.insert(0, self.profile_data["name"])
        self.owner_name_entry.pack(pady=(8, 0), padx=25, fill="x", expand=True)

        self.owner_age_entry = tk.CTkEntry(self.card_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray")
        self.owner_age_entry.insert(0, self.profile_data["age"])
        self.owner_age_entry.pack(pady=8, padx=25, fill="x", expand=True)

        self.owner_city_entry = tk.CTkEntry(self.card_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray")
        self.owner_city_entry.insert(0, self.profile_data["city"])
        self.owner_city_entry.pack(pady=0, padx=25, fill="x", expand=True)

        self.owner_interests_entry = tk.CTkEntry(self.card_frame, font=tk.CTkFont(size=14), justify="left", text_color="black", fg_color="gray")
        self.owner_interests_entry.insert(0, ", ".join(self.profile_data["interests"]))
        self.owner_interests_entry.pack(pady=8, padx=25, fill="x", expand=True)

        # BIO
        if self.profile_data.get("bio"):
            self.bio_entry = tk.CTkEntry(self.card_frame, font=tk.CTkFont(size=12), justify="left", text_color="black", fg_color="gray")
            self.bio_entry.insert(0, self.profile_data["bio"])
            self.bio_entry.pack(pady=(0, 30), padx=25, fill="x", expand=True)
    
    
    def select_image(self):
        """Öffnet Dateiauswahl NUR für PNG"""
        file_path = filedialog.askopenfilename(
            title="Profilbild auswählen (PNG)",
            filetypes=[("PNG Bilder", "*.png")]  # NUR PNG
        )
        
        if file_path:
            try:
                # Bild laden und skalieren
                img = Image.open(file_path)
                img.thumbnail((200, 250), Image.Resampling.LANCZOS)
                
                preview = tk.CTkToplevel()
                preview.title("Profilbild Vorschau")
                preview.attributes("-topmost", True)
                preview.geometry("250x350")

                # Als CTkImage für Vorschau
                self.profile_img = tk.CTkImage(light_image=img, dark_image=img, size=(200, 250))
                profile_img_preview_label = tk.CTkLabel(preview, image=self.profile_img, text="")
                profile_img_preview_label.pack(pady=10)

                # Bestätigung
                confirm_img = tk.CTkButton(preview ,text=f"✅ {os.path.basename(file_path)}", text_color="#4CAF50", command=lambda: [self.save_profile_image(file_path), preview.destroy()])
                confirm_img.pack(pady=10)
                
            except Exception as e:
                MessageWindow("Fehler", f"PNG konnte nicht geladen werden:\n{str(e)}")

    def save_profile_image(self, file_path):
        """Kopiert ausgewähltes PNG ins img/ Verzeichnis"""
        if file_path:
            try:
                # img/ Ordner erstellen
                os.makedirs("img", exist_ok=True)
                
                # Zielpfad
                new_path = f"img/profile_{self.profile_data['id']}.png"
                
                # Original skalieren und als PNG speichern
                img = Image.open(file_path)
                img.thumbnail((400, 500), Image.Resampling.LANCZOS)
                img.save(new_path, "PNG", quality=95)
                
                # Im Profil speichern
                self.profile_data["profile_image"] = new_path
                return True
                
            except Exception as e:
                MessageWindow("Fehler", f"PNG konnte nicht gespeichert werden:\n{str(e)}")
                return False
        return False
    
    
    def save(self):
        # Dog
        self.profile_data["dog"]["name"] = self.dog_name_entry.get()
        self.profile_data["dog"]["age_years"] = int(self.dog_age_entry.get())
        self.profile_data["dog"]["sex"] = self.dog_sex_entry.get()
        self.profile_data["dog"]["description"] = self.dog_info_entry.get()


        # User
        self.profile_data["name"] = self.owner_name_entry.get()
        self.profile_data["age"] = self.owner_age_entry.get()
        self.profile_data["city"] = self.owner_city_entry.get()
        self.profile_data["interests"] = self.owner_interests_entry.get().split(", ")
        if len(self.card_frame.winfo_children()) > 7:
            self.profile_data["bio"] = self.bio_entry.get()
        self.storage.save()