# modules/ui_chats_overview.py - EINZES FENSTER, KEINE NEW CHAT BUTTONS
import customtkinter as tk
from datetime import datetime

from modules.storage import Storage

class ChatsOverview(tk.CTkToplevel):
    def __init__(self, storage: Storage, current_user_id: int):
        super().__init__()
        self.storage = storage
        self.current_user_id = current_user_id
        self.title("Chats")
        self.geometry("700x700")
        self.selected_chat = None
        self.attributes("-topmost", True)
        
        self.build_widgets()
        self.refresh_chat_list()

    def build_widgets(self):
        """Layout: Sidebar (links) + Chat RECHTS IM GLEICHEN FENSTER"""
        # Haupt-Grid
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (linke Spalte)
        self.sidebar_frame = tk.CTkFrame(self, width=280)
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe", padx=(10, 10))
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        # Sidebar Header (NUR "Chats")
        header_frame = tk.CTkFrame(self.sidebar_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        
        tk.CTkLabel(header_frame, text="Chats", 
                   font=tk.CTkFont(size=22, weight="bold")).pack(pady=12)

        # Chat-Liste
        self.chats_list_frame = tk.CTkScrollableFrame(self.sidebar_frame)
        self.chats_list_frame.grid(row=1, column=0, sticky="nswe", padx=15, pady=(0, 15))
        self.chats_list_frame.grid_columnconfigure(0, weight=1)

        # CHAT RECHTS (IM GLEICHEN FENSTER)
        self.chat_frame = tk.CTkFrame(self)
        self.chat_frame.grid(row=0, column=1, sticky="nswe", padx=(0, 10))
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(1, weight=1)

        # Chat Header
        self.chat_header = tk.CTkFrame(self.chat_frame)
        self.chat_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))
        
        self.chat_title = tk.CTkLabel(self.chat_header, text="Wähle einen Chat aus", 
                                    font=tk.CTkFont(size=22, weight="bold"))
        self.chat_title.pack()

        # Nachrichtenbereich
        self.messages_frame = tk.CTkScrollableFrame(self.chat_frame, fg_color="#f8f9fa")
        self.messages_frame.grid(row=1, column=0, sticky="nswe", padx=20, pady=(0, 20))
        self.messages_frame.grid_columnconfigure(0, weight=1)

        # Eingabebereich
        self.input_frame = tk.CTkFrame(self.chat_frame)
        self.input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = tk.CTkEntry(self.input_frame, placeholder_text="Nachricht eingeben...")
        self.message_entry.grid(row=0, column=0, sticky="ew", padx=(15, 10), pady=15)
        self.message_entry.bind("<Return>", self.send_message)
        self.message_entry.configure(state="disabled")  # Bis Chat ausgewählt

        send_btn = tk.CTkButton(self.input_frame, text="Senden", command=self.send_message, width=90)
        send_btn.grid(row=0, column=1, sticky="e", padx=(0, 15), pady=15)

    def refresh_chat_list(self):
        """Chat-Liste aktualisieren"""
        for widget in self.chats_list_frame.winfo_children():
            widget.destroy()

        chats = self.storage.data.get("chats", [])
        for chat in chats:
            if self.is_my_chat(chat):
                self.create_chat_button(chat)

    def is_my_chat(self, chat):
        return chat["user1_id"] == self.current_user_id or chat["user2_id"] == self.current_user_id

    def create_chat_button(self, chat):
        """Chat-Button ohne New-Chat-Shit"""
        other_user_id = chat["user2_id"] if chat["user1_id"] == self.current_user_id else chat["user1_id"]
        other_user_name = self.find_user_name(other_user_id)
        
        messages = chat.get("messages", [])
        last_msg = messages[-1]["text"][:30] + "..." if messages else "Keine Nachrichten"
        
        # Einfacher Chat-Button
        chat_btn = tk.CTkButton(
            self.chats_list_frame,
            text=f"🐕 {other_user_name}\n{last_msg}",
            font=tk.CTkFont(size=14),
            fg_color="gray",
            hover_color="lightgray",
            anchor="w",
            command=lambda c=chat: self.select_chat(c),
            height=70,
            corner_radius=12,
            text_color="black"
        )
        chat_btn.pack(fill="x", padx=10, pady=5)

    def find_user_name(self, user_id):
        for user in self.storage.data.get("users", []):
            if user["id"] == user_id:
                return user["name"]
        return "Unbekannt"

    def select_chat(self, chat):
        """Lädt Chat RECHTS (kein neues Fenster!)"""
        self.selected_chat = chat
        other_user_id = chat["user2_id"] if chat["user1_id"] == self.current_user_id else chat["user1_id"]
        
        # Header updaten
        self.chat_title.configure(text=f"🐕 {self.find_user_name(other_user_id)}")
        
        # Nachrichten laden
        self.clear_messages()
        messages = chat.get("messages", [])
        for msg in messages:
            self.add_message(msg["text"], msg["sender_id"] == self.current_user_id)
        
        # Input freigeben
        self.message_entry.configure(state="normal")

    def clear_messages(self):
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

    def add_message(self, text, is_own):
        """Nachricht hinzufügen"""
        msg_frame = tk.CTkFrame(self.messages_frame, fg_color="transparent")
        msg_frame.pack(fill="x", padx=20, pady=8)
        
        if is_own:
            # Rechts (eigen)
            msg = tk.CTkLabel(msg_frame, text=text, fg_color="#007AFF", text_color="white",
                            corner_radius=18, padx=20, pady=12)
            msg.pack(anchor="e")
        else:
            # Links (fremd)
            msg = tk.CTkLabel(msg_frame, text=text, fg_color="#E8ECEF", text_color="black",
                            corner_radius=18, padx=20, pady=12)
            msg.pack(anchor="w")

    def send_message(self, event=None):
        if not self.selected_chat:
            return
            
        text = self.message_entry.get().strip()
        if not text:
            return

        # Anzeigen
        self.add_message(text, True)
        
        # Speichern
        new_msg = {
            "id": len(self.selected_chat.get("messages", [])) + 1,
            "chat_id": self.selected_chat["id"],
            "sender_id": self.current_user_id,
            "receiver_id": self.selected_chat["user2_id"] if self.selected_chat["user1_id"] == self.current_user_id else self.selected_chat["user1_id"],
            "text": text,
            "timestamp": datetime.now().isoformat()
        }
        
        if "messages" not in self.selected_chat:
            self.selected_chat["messages"] = []
        self.selected_chat["messages"].append(new_msg)
        self.storage.save()
        
        self.message_entry.delete(0, "end")