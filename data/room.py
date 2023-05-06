
from dataclasses import dataclass
import random

from data.user import User
from utils.string_utils import random_string

# Since the SID changes every refresh, browser change,etc (i think)
# there's no point in having it in the "User" class
# so made a quick wrapper here for that 
@dataclass
class UserSidWrapper:
    user: User
    sid: str
    

class Room:
    id: str
    public: bool # to implement
    password: str | None # to implement
    current_video: str 
    users_sid: list[UserSidWrapper]

    def __init__(self, id: str, public: bool = False, password: str | None = None) -> None:
        self.id = id
        self.public = public
        self.password = password
        self.current_video = ""
        self.users_sid = []

    def get_usersid(self, user: User) -> UserSidWrapper:
        for user_sid in self.users_sid:
            if user_sid.user == user:
                return user_sid
        return None


class RoomManager:
    rooms: list[Room]
    def __init__(self) -> None:
        self.rooms = []
    
    VALID_ROOM_CHARS = "0123456789"
    ROOM_CHARS_LENGTH = 7
    def _get_random_room_number(self) -> str:
        result = random_string(self.VALID_ROOM_CHARS, self.ROOM_CHARS_LENGTH)
        while self.get_room(result):
            result = random_string(self.VALID_ROOM_CHARS, self.ROOM_CHARS_LENGTH)
        return result

    def get_room(self, id: str) -> Room | None:
        for room in self.rooms:
            if room.id == id:
                return room
        return None
    
    # This is quite inefficient
    # But can't think of a better way to do this
    # that doesn't resolve over a circular import
    # but oh well
    def get_room_from_user(self, user: User) -> Room | None:
        for room in self.rooms:
            for user_sid in room.users_sid:
                if user_sid.user == user:
                    return room
        return None

    def new_room(self) -> Room:
        room = Room(
            id=self._get_random_room_number(),
        )
        self.rooms.append(room)
        return room
    