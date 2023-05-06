from flask import request
from data.room import Room, RoomManager, UserSidWrapper
from data.user import User, UserManager
from data.vars import Vars
from utils.string_utils import ALPHABET_NUMBERS, random_string

# Unwrapping values for easier use
socketio = Vars.socketio
user_manager = Vars.user_manager
room_manager = Vars.room_manager

def emit_to_user(usersid: UserSidWrapper, message: str, data: dict | str) -> None:
    socketio.emit(message, data, room=usersid.sid) 

# tbh can prolly use the room thing waaay bettter
# but not sure how it works w flask and don't rly want to bother
def emit_to_room(room: Room, message: str, data: dict | str, ommited_user: User | None) -> None:
    for usersid in room.users_sid:
        if usersid.user != ommited_user:
            emit_to_user(usersid, message, data)

infoRequests: dict[str, UserSidWrapper] = {}

@socketio.on("joinRoom")
def join_room(data):
    user = user_manager.get_user_from_userid(data["user_id"])
    room = room_manager.get_room(data['room_id']) 
    if user == None or room == None: return

    current_sid = request.sid

    userSid = room.get_usersid(user)
    if userSid:
        userSid.sid = current_sid
    else:
        userSid = UserSidWrapper(user, current_sid)
        room.users_sid.append(userSid)
    
    # invalidate other UserSidWrappers
    for r in room_manager.rooms: 
        if r == room: continue
        for user_sid in r.users_sid:
            if user_sid.user.id == user.id:
                print(f"Invalidated room {r.id} for user {user.name}.")
                r.users_sid.remove(user_sid)
    
    print(f"{user.name} joined room {room.id}.")
    
    if len(room.users_sid) > 1: # if not alone 
        update_id = random_string(ALPHABET_NUMBERS, 15)
        infoRequests[update_id] = userSid
        emit_to_room(room, "userJoin", {"name": user.name, "update_id": update_id}, user)


@socketio.on("play")
def play(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return

    emit_to_room(room, "play", {"user": user.name}, user)


@socketio.on("pause")
def pause(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return

    emit_to_room(room, "pause", {"user": user.name}, user)


@socketio.on("updateTime")
def update_time(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return

    emit_to_room(room, "timeUpdate", {"user": user.name, "time": data["time"], "reason": data["reason"]}, user)


@socketio.on("setVideo")
def set_video(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return
    
    emit_to_room(room, "videoSet", {"user": user.name, "video": data["video"]}, user)


@socketio.on("roomData")
def room_data_receive(data):
    update_id = data["update_id"]
    user_sid = infoRequests.get(update_id)
    if not user_sid:
        # Note that this is sent back from all clients
        # (to have the fastest response & avoid having a dead client just send back nothing)
        # So once the first response is proceeded, the user_sid won't be present anymore in the dict
        return
    
    infoRequests.pop(update_id)
    # could create another emit but meh lmao just sending everything
    emit_to_user(user_sid, "videoSet", {"user": "sync", "video": data["video_src"]})
    emit_to_user(user_sid, "timeUpdate", {"user": "sync", "reason": "initialLoad", "time": data["video_time"]})
    message = "pause" if data["paused"] else "play"
    emit_to_user(user_sid, message, {"user": "sync"})
    print(data)