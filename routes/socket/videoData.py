

from data.room import Room
from data.vars import Vars
from routes.socket_route_utils import emit_video_data, video_data_requests

user_manager = Vars.user_manager
room_manager = Vars.room_manager
socketio = Vars.socketio

def set_current_room_video(room: Room, data: dict):
    video = room.current_video
    video.name = data.get("video_name")
    video.src = data.get("video_src")
    video.time = data.get("video_time")
    video.paused = True if data.get("paused") else False
    return video

@socketio.on("videoData")
def room_data_receive(data):
    update_id = data.get("update_id")
    room_user = video_data_requests.get(update_id)
    if not room_user:
        # Note that this is sent back from all clients
        # (to have the fastest response & avoid having a dead client just send back nothing)
        # So once the first response is proceeded, the user_sid won't be present anymore in the dict
        return
    
    video_data_requests.pop(update_id)

    room = room_manager.get_room_from_user(room_user.user)
    video = set_current_room_video(room, data)

    emit_video_data(room_user, video)