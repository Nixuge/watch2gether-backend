from data.room import COMMAND
from data.vars import Vars
from routes.socket_route_utils import emit_to_room, get_room_user_from_dict

socketio = Vars.socketio
user_manager = Vars.user_manager
room_manager = Vars.room_manager

@socketio.on("updateTime")
def update_time(data):
    user, room = get_room_user_from_dict(data)
    if user == None or room == None: return

    room_user = room.get_usersid(user)

    if COMMAND.time in room_user.timeouts:
        room_user.timeouts.remove(COMMAND.time)
        return

    video = room.current_video
    video.time = data.get("time")

    room.run_timeout_all_users(COMMAND.time)
    emit_to_room(room, "timeUpdate", {"user": user.name, "time": video.time, "reason": data.get("reason")}, user)