from data.vars import Vars
from routes.socket_route_utils import emit_to_room

user_manager = Vars.user_manager
room_manager = Vars.room_manager
socketio = Vars.socketio

@socketio.on("play")
def play(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return

    room.current_video.paused = False
    emit_to_room(room, "play", {"user": user.name}, user)


@socketio.on("pause")
def pause(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return

    room.current_video.paused = True
    emit_to_room(room, "pause", {"user": user.name}, user)