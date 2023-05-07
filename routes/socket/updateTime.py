from data.vars import Vars
from routes.socket_route_utils import emit_to_room

socketio = Vars.socketio
user_manager = Vars.user_manager
room_manager = Vars.room_manager

@socketio.on("updateTime")
def update_time(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return

    emit_to_room(room, "timeUpdate", {"user": user.name, "time": data["time"], "reason": data["reason"]}, user)