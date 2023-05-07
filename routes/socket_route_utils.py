from data.room import Room, UserSidWrapper
from data.user import User
from data.vars import Vars

socketio = Vars.socketio

def emit_to_user(usersid: UserSidWrapper, message: str, data: dict | str) -> None:
    socketio.emit(message, data, room=usersid.sid) 

def emit_to_user_str(sid: str, message: str, data: dict | str) -> None:
    socketio.emit(message, data, room=sid) 

# tbh can prolly use the room thing waaay bettter
# but not sure how it works w flask and don't rly want to bother
def emit_to_room(room: Room, message: str, data: dict | str, ommited_user: User | None) -> None:
    for usersid in room.users_sid:
        if usersid.user != ommited_user:
            emit_to_user(usersid, message, data)

video_data_requests: dict[str, UserSidWrapper] = {}