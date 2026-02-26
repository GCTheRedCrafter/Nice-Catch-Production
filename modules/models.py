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
    password: str
    age: int
    city: str
    bio: str
    interests: List[str]
    dog: Dog
    seen_profiles: List[str] = field(default_factory=list)

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