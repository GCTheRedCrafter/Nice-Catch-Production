import customtkinter as tk
from PIL import Image

from modules.ui_utils import MessageWindow
from modules.storage import Storage
from modules.logic import Matcher

class NiceCatchApp(tk.CTk):
    def __init__(self, current_user_id=1):
        super().__init__()
        self.title("NiceCatch")
        self.geometry("500x800")
        self.storage = Storage()
        self.matcher = Matcher(self.storage, current_user_id)
        self.current_profile = None
        self.last_profile_id = None

        self.build_widgets()
        self.load_next_profile()

    def build_widgets(self):
        """NUR Header + Buttons - KEINE Profile"""
        # Hauptfenster konfigurieren
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # HEADER (Row 0)
        self.chat_btn = tk.CTkButton(self, text="💬 Chats", command=self.open_chats)
        self.chat_btn.grid(row=0, column=2, sticky="ne", padx=(5, 10), pady=10)

        self.title_label = tk.CTkLabel(self, text="NiceCatch", font=tk.CTkFont(size=24, weight="bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="nw", padx=10, pady=10)

        self.profile_btn = tk.CTkButton(self, text="👤 Profil", 
            command=lambda: MessageWindow("Profil", 
                f"Du bist eingeloggt als: {self.storage.data['users'][self.matcher.current_user_id - 1]['name']}"
            )
        )
        self.profile_btn.grid(row=0, column=1, sticky="ne", padx=(150, 5), pady=10)

        # SCROLLABLE FRAME (leer lassen)
        self.card_frame = tk.CTkScrollableFrame(self, fg_color="gray90", corner_radius=15)
        self.card_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=15, pady=15)
        self.card_frame.grid_columnconfigure(0, weight=1)

        # BUTTONS (Row 2 + 3)
        self.btn_frame = tk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.grid(row=2, column=0, columnspan=3, sticky="ew", padx=15, pady=10)
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        
        self.dislike_btn = tk.CTkButton(self.btn_frame, text="❌", fg_color="red",
                                        command=self.skip_profile, height=50)
        self.dislike_btn.grid(row=0, column=0, sticky="ew", padx=(20,10), pady=15)
        
        self.like_btn = tk.CTkButton(self.btn_frame, text="⚽", fg_color="limegreen",
                                    command=self.like_profile, height=50)
        self.like_btn.grid(row=0, column=1, sticky="ew", padx=(10,20), pady=15)



    def clear_card_content(self):
        """Löscht ALLE Widgets aus Scrollable Frame"""
        for widget in self.card_frame.winfo_children():
            widget.destroy()

    def load_next_profile(self):
        """Lädt EIN MAL Profil in Scrollable Frame"""
        self.current_profile = self.matcher.get_next_profile(self.last_profile_id)
        if not self.current_profile:
            self.clear_card_content()
            placeholder = tk.CTkLabel(self.card_frame, text="Keine Profile mehr 😢", 
                                    font=tk.CTkFont(size=18))
            placeholder.pack(expand=True, pady=50)
            return

        # 1x Widgets löschen
        self.clear_card_content()
        
        # PROFILFOTO
        try:
            img_path = f"img/profile_{self.current_profile['id']}.png"
            profile_image = Image.open(img_path)
        except FileNotFoundError:
            try:
                profile_image = Image.open("img/logo.jpeg")
            except:
                profile_image = None

        if profile_image:
            profile_img = tk.CTkImage(light_image=profile_image, dark_image=profile_image, size=(140, 180))
            picture_label = tk.CTkLabel(self.card_frame, image=profile_img, text="")
            picture_label.pack(pady=20)
        else:
            picture_label = tk.CTkLabel(self.card_frame, text="🐕", font=tk.CTkFont(size=80))
            picture_label.pack(pady=20)

        # NAME
        dog = self.current_profile["dog"]
        name_label = tk.CTkLabel(self.card_frame, 
                            text=f'{dog["name"]} – {dog["age_years"]} Jahre, {dog["sex"]}', 
                            font=tk.CTkFont(size=22, weight="bold"))
        name_label.pack(pady=(0, 15), padx=25)

        # INFO
        info_text = f'👤 {self.current_profile["name"]}, {self.current_profile["age"]} Jahre\n' \
                f'📍 {self.current_profile["city"]}\n' \
                f'🎾 {", ".join(self.current_profile["interests"])}'
        info_label = tk.CTkLabel(self.card_frame, text=info_text,
                            font=tk.CTkFont(size=14), justify="left")
        info_label.pack(pady=20, padx=25)

        # BIO
        if self.current_profile.get("bio"):
            bio_label = tk.CTkLabel(self.card_frame, text=self.current_profile["bio"],
                                font=tk.CTkFont(size=12), justify="left")
            bio_label.pack(pady=(0, 30), padx=25)

    def skip_profile(self):
        self.load_next_profile()

    def like_profile(self):
        if not self.current_profile:
            return
        chat_id = self.matcher.like_user(self.current_profile["id"])
        if chat_id:
            MessageWindow("🎉 Match!", f"Du hast ein Match! Chat-ID: {chat_id}")
        self.load_next_profile()
        
    def open_chats(self):
        MessageWindow("Chats", "Chats werden hier implementiert...")

if __name__ == "__main__":
    app = NiceCatchApp()
    app.mainloop()