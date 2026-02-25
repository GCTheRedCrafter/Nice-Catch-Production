from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Dog:
    id: int
    name: str
    age_years: int
    sex: str          # "Rüde" oder "Hündin"
    friendly: bool
    dislikes_water: bool
    description: str = ""

@dataclass
class UserProfile:
    id: int
    name: str
    age: int
    city: str
    bio: str
    interests: List[str]
    dog: Dog

@dataclass
class Match:
    id: int
    user1_id: int
    user2_id: int
    created_at: str
    is_mutual: bool = False

@dataclass
class Message:
    id: int
    chat_id: int
    sender_id: int
    receiver_id: int
    text: str
    timestamp: datetime

@dataclass
class Chat:
    id: int
    user1_id: int
    user2_id: int
    messages: List[Message] = field(default_factory=list)

if __name__ == "__main__":
    from pprint import pprint
    # kleiner Selbsttest
    from datetime import datetime
    mia_dog = Dog(
        id=1,
        name="Bailey",
        age_years=4,
        sex="Rüde",
        friendly=True,
        dislikes_water=True,
        description="Mag Spaziergänge, ist freundlich, aber kein Fan von Wasser."
    )

    mia = UserProfile(
        id=1,
        name="Mia",
        age=55,
        city="Nähe Bielefeld",
        bio="Offen, herzlich und humorvoll. Freue mich auf nette Gassi‑Kontakte.",
        interests=["Spaziergänge", "Natur", "gute Gespräche"],
        dog=mia_dog
)
    pprint(mia)