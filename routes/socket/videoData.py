

from data.room import UserSidWrapper
from data.vars import Vars
from data.video import Video
from routes.socket_route_utils import emit_to_user, video_data_requests

user_manager = Vars.user_manager
room_manager = Vars.room_manager
socketio = Vars.socketio

def emit_video_data(user_sid: UserSidWrapper, data: dict):
    # could create another packet but meh, sending 3 diff packets isn't that bad
    emit_to_user(user_sid, "videoSet", {"user": "sync", "video": data["video_src"]})
    emit_to_user(user_sid, "timeUpdate", {"user": "sync", "reason": "initialLoad", "time": data["video_time"]})
    message = "pause" if data["paused"] else "play"
    emit_to_user(user_sid, message, {"user": "sync"})

def set_current_room_video():
    pass

@socketio.on("videoData")
def room_data_receive(data):
    update_id = data["update_id"]
    user_sid = video_data_requests.get(update_id)
    if not user_sid:
        # Note that this is sent back from all clients
        # (to have the fastest response & avoid having a dead client just send back nothing)
        # So once the first response is proceeded, the user_sid won't be present anymore in the dict
        return
    room = room_manager.get_room_from_user(user_manager.get_user_from_flask_dict(data))
    if not room.current_video:
        # room.current_video = Video(name)
        set_current_room_video()
    print(room.current_video)
    video_data_requests.pop(update_id)

    emit_video_data(user_sid, data)