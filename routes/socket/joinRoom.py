from flask import request
from data.room import UserSidWrapper
from data.vars import Vars
from routes.socket_route_utils import emit_to_room, emit_to_user_str, video_data_requests
from utils.string_utils import ALPHABET_NUMBERS, random_string

user_manager = Vars.user_manager
room_manager = Vars.room_manager

@Vars.socketio.on("joinRoom")
def join_room(data):
    user = user_manager.get_user_from_userid(data.get("user_id"))
    room = room_manager.get_room(data.get("room_id")) 
    current_sid = request.sid

    if user == None or room == None: 
        emit_to_user_str(current_sid, "roomStatus", "invalid")
        return


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
    
    emit_to_user_str(current_sid, "roomStatus", "valid")

    if len(room.users_sid) > 1: # if not alone 
        update_id = random_string(ALPHABET_NUMBERS, 15)
        video_data_requests[update_id] = userSid
        emit_to_room(room, "userJoin", {"name": user.name, "update_id": update_id}, user)