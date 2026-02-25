import json
from datetime import datetime
from dataclasses import asdict

from models import UserProfile, Dog, Match, Chat, Message

class Storage:
    def __init__(self, path="nicecatch_data.json"):
        self.path = path
        self.data = {"users": [], "matches": [], "chats": []}
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

if __name__ == "__main__":

    s = Storage()


    mia_dog = Dog(
        id=2,
        name="Lea",
        age_years=7,
        sex="Hündin",
        friendly=True,
        dislikes_water=True,
        description="Mag Spaziergänge, ist freundlich, aber kein Fan von Wasser."
    )

    mia = UserProfile(
        id=2,
        name="Lena",
        age=55,
        city="Nähe München",
        bio="Offen, herzlich und humorvoll. Freue mich auf nette Gassi-Kontakte.",
        interests=["Spaziergänge", "Natur", "gute Gespräche"],
        dog=mia_dog
    )

    s.add_user(mia)
    print("Mia wurde angelegt.")