from data.vars import Vars
from routes.socket_route_utils import emit_to_room

socketio = Vars.socketio
user_manager = Vars.user_manager
room_manager = Vars.room_manager

@socketio.on("setVideo")
def set_video(data):
    user = user_manager.get_user_from_flask_dict(data)
    room = room_manager.get_room_from_user(user)
    if user == None or room == None: return
    
    video = room.current_video
    video.src = data.get("video_src")
    video.name = data.get("video_name")
    emit_to_room(room, "videoSet", {"user": user.name, "video_name": video.name, "video_src": video.src}, user)