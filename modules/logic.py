from datetime import datetime
from modules.models import Match, Chat
from modules.storage import Storage

class Matcher:
    def __init__(self, storage: Storage, current_user_id: int):
        self.storage = storage
        self.current_user_id = current_user_id

    def get_next_profile(self, last_user_id):
        # sehr einfache Version: irgend ein anderes Profil zurückgeben
        if last_user_id is None:
             last_user_id = 0
        for u in self.storage.data["users"]:
            if u["id"] != self.current_user_id and u["id"] > last_user_id and u["id"] not in self.storage.data["users"][self.current_user_id-1]["seen_profiles"]:
                self.storage.data["users"][self.current_user_id-1]["seen_profiles"].append(u["id"])
                self.storage.save()
                return u
        return None

    def like_user(self, other_user_id: int):
        # hier würdest du prüfen, ob der andere dich schon geliked hat
        match = Match(
            id=len(self.storage.data["matches"]) + 1,
            user1_id=self.current_user_id,
            user2_id=other_user_id,
            created_at=str(datetime.now()),
            is_mutual=True  # für den Anfang einfach direkt Match
        )
        self.storage.data["matches"].append(match.__dict__)
        self.storage.save()
        # Chat automatisch anlegen
        chat = Chat(
            id=len(self.storage.data["chats"]) + 1,
            user1_id=self.current_user_id,
            user2_id=other_user_id
        )
        for c in self.storage.data["matches"]:
            if c["user2_id"] == self.current_user_id and c["user1_id"] == other_user_id:
                self.storage.data["chats"].append(
                    {"id": chat.id, "user1_id": chat.user1_id,
                     "user2_id": chat.user2_id, "messages": []}
                )
                self.storage.save()
                return chat.id
        return None

def check_password(storage: Storage, username: str, password: str):
    for user in storage.data["users"]:
        if user["name"] == username and user["password"] == password:
            return user["id"]
    return None