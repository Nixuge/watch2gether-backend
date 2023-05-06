from dataclasses import dataclass
import random
from typing import Any

@dataclass
class User:
    name: str
    id: str
    # sid: str

# Note: both RoomManager & UserManager similar but too lazy to use inheritance
# Quite a lot of duplicate code anyways, but that's how it is
class UserManager:
    users: list[User]
    def __init__(self) -> None:
        self.users = []
    
    VALID_CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
    CHARS_LENGTH_COOKIE = 10
    def _get_random_cookie(self) -> str:
        result = ''.join(random.choice(self.VALID_CHARS) for _ in range(self.CHARS_LENGTH_COOKIE))
        while self.get_user_from_userid(result):
            result = ''.join(random.choice(self.VALID_CHARS) for _ in range(self.CHARS_LENGTH_COOKIE))
        return result
    
    VALID_NUMS = "0123456789"
    CHARS_LENGTH_USERNAME = 5
    def _get_random_username(self) -> str:
        result = "User " + ''.join(random.choice(self.VALID_NUMS) for _ in range(self.CHARS_LENGTH_USERNAME))
        while self.get_user_from_name(result):
            result = "User " + ''.join(random.choice(self.VALID_NUMS) for _ in range(self.CHARS_LENGTH_USERNAME))
        return result

    def get_user_from_name(self, name: str) -> User | None:
        for user in self.users:
            if user.name == name:
                return user
        return None  

    def get_user_from_userid(self, user_id: str) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user
        return None  

    def get_user_from_flask_dict(self, data: dict) -> User | None:
        user_id = data.get("user_id")
        return self.get_user_from_userid(user_id)

    def new_user(self) -> User:
        user = User(
            name=self._get_random_username(),
            id=self._get_random_cookie()
        )
        self.users.append(user)
        return user