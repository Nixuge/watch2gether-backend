from data.room import Room, RoomUser
from data.user import User
from data.vars import Vars
from data.video import Video

socketio = Vars.socketio
user_manager = Vars.user_manager
room_manager = Vars.room_manager

def emit_to_user(room_user: RoomUser, message: str, data: dict | str) -> None:
    socketio.emit(message, data, room=room_user.sid) 

def emit_to_user_str(sid: str, message: str, data: dict | str) -> None:
    socketio.emit(message, data, room=sid) 

# tbh can prolly use the room thing waaay bettter
# but not sure how it works w flask and don't rly want to bother
def emit_to_room(room: Room, message: str, data: dict | str, ommited_user: User | None) -> None:
    for room_user in room.room_users:
        if room_user.user != ommited_user:
            emit_to_user(room_user, message, data)

#TODO: put that inside the room class
video_data_requests: dict[str, RoomUser] = {}

def emit_video_data(room_user: RoomUser, video: Video):
    # could create another packet but meh, sending 3 diff packets isn't that bad
    emit_to_user(room_user, "videoSet", {"user": "sync", "video_name": video.name, "video_src": video.src})
    emit_to_user(room_user, "timeUpdate", {"user": "sync", "reason": "initialLoad", "time": video.time})
    message = "pause" if video.paused else "play"
    emit_to_user(room_user, message, {"user": "sync"})


def get_user_room_from_dict(data: dict) -> tuple[User, Room]:
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    return user, room