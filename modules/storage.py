import json
from datetime import datetime
from dataclasses import asdict

#from modules.models import UserProfile, Dog, Match, Chat, Message

class Storage:
    def __init__(self, path="nicecatch_data.json"):
        self.path = path
        self.data = {"users": [], "matches": [], "chats": [], "messages": []}
        self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
            self.data = raw
        except FileNotFoundError:
            self.save()

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_user(self, user_obj):
        user_dict = asdict(user_obj)
        self.data["users"].append(user_dict)
        self.save()
    
    def reset(self):
        self.data = {"users": self.data["users"], "matches": [], "chats": [], "messages": []}
        self.save()

if __name__ == "__main__":
    storage = Storage()
    storage.reset()