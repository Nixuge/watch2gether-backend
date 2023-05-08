
import asyncio
from data.user import User
from data.video import Video
from utils.string_utils import random_string

# Since the SID changes every refresh, browser change,etc (i think)
# there's no point in having it in the "User" class
# so made a quick wrapper here for that 

class COMMAND:
    time = 1
    playpause = 2
    

# Basically a wrapper for the User class
# but with room specific vars like the SID and the timeouts
class RoomUser:
    user: User
    sid: str
    timeouts = list[COMMAND]
    def __init__(self, user: User, sid: str):
        self.user = user
        self.sid = sid
        self.timeouts = []

class Room:
    id: str
    public: bool # to implement
    password: str | None # to implement
    current_video: Video 
    room_users: list[RoomUser]

    def __init__(self, id: str, public: bool = False, password: str | None = None) -> None:
        self.id = id
        self.public = public
        self.password = password
        self.current_video = Video("Default video", "http://localhost:2135/static/test.mp4", 0, True)
        self.room_users = []

    def run_timeout_all_users(self, command: COMMAND, exempt: User | None = None):
        for user in self.room_users:
            if user == exempt: continue
            if not command in user.timeouts:
                user.timeouts.append(command)
        
        loop = asyncio.get_event_loop()
        loop.create_task(self._remove_timeout_all_users(command))
    
    async def _remove_timeout_all_users(self, command: COMMAND, delay: float = .3):
        await asyncio.sleep(delay)
        for user in self.room_users:
            if command in user.timeouts:
                user.timeouts.remove(command)

    def get_room_user(self, user: User) -> RoomUser:
        for room_user in self.room_users:
            if room_user.user == user:
                return room_user
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
            for room_user in room.room_users:
                if room_user.user == user:
                    return room
        return None

    def new_room(self) -> Room:
        room = Room(
            id=self._get_random_room_number(),
        )
        self.rooms.append(room)
        return room
    