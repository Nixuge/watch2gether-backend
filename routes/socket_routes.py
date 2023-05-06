from flask import request
from room import Room, RoomManager, UserSidWrapper
from user import User, UserManager
from vars import Vars

# Unwrapping values for easier use
socketio = Vars.socketio
user_manager = Vars.user_manager
room_manager = Vars.room_manager


# tbh can prolly use the room thing waaay bettter
# but not sure how it works w flask and don't rly want to bother
def emit_to_room(room: Room, message: str, data: dict | str, ommited_user: User | None) -> None:
    for usersid in room.users_sid:
        if usersid.user == ommited_user: continue
        socketio.emit(message, data, room=usersid.sid) 


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
        room.users_sid.append(UserSidWrapper(user, current_sid))
    
    # invalidate other UserSidWrappers
    for r in room_manager.rooms: 
        if r == room: continue
        for user_sid in r.users_sid:
            if user_sid.user.id == user.id:
                print(f"Invalidated room {r.id} for user {user.name}.")
                r.users_sid.remove(user_sid)
    
    print(f"{user.name} joined room {room.id}.")

    emit_to_room(room, "userJoin", user.name, user)


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