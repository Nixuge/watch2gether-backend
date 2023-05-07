from flask import request
from data.room import UserSidWrapper
from data.vars import Vars
from routes.socket_route_utils import emit_to_room, emit_to_user_str, emit_video_data, video_data_requests
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


    user_sid = room.get_usersid(user)
    if user_sid:
        user_sid.sid = current_sid
    else:
        user_sid = UserSidWrapper(user, current_sid)
        room.users_sid.append(user_sid)
    
    # invalidate other UserSidWrappers
    for i_room in room_manager.rooms: 
        if i_room == room: continue
        for i_user_sid in i_room.users_sid:
            if i_user_sid.user.id == user.id:
                print(f"Invalidated room {i_room.id} for user {user.name}.")
                i_room.users_sid.remove(i_user_sid)
    
    print(f"{user.name} joined room {room.id}.")
    
    emit_to_user_str(current_sid, "roomStatus", "valid")

    if len(room.users_sid) > 1: # if not alone 
        update_id = random_string(ALPHABET_NUMBERS, 15)
        video_data_requests[update_id] = user_sid
        emit_to_room(room, "userJoin", {"name": user.name, "update_id": update_id}, user)
    
    # Send a video data packet at joinRoom, then wait for another user to send its packet
    # This is made so that initial video loadings are usually quicker
    # & so that if no one responds, you still get a source
    emit_video_data(user_sid, room.current_video)