


import os
from pprint import pprint
from flask import Flask, jsonify, make_response, redirect, render_template, request
from flask_socketio import SocketIO
from room import Room, RoomManager, UserSidWrapper

from user import User, UserManager

# def main():
app = Flask(__name__)
socketio = SocketIO(app,cors_allowed_origins="*")

user_manager = UserManager() # Could've been made static
room_manager = RoomManager() # same
rooms = {}

def add_userid_request(resp) -> User:
    user_id = request.cookies.get("user_id")
    user = None
    if user_id:
        user = user_manager.get_user_from_userid(user_id)
    if not user or not user_id:
        user = user_manager.new_user()
        resp.set_cookie("user_id", user.id, path="/")
    # return user


# tbh can prolly use the room thing waaay bettter
# but not sure how it works w flask and don't rly want to bother
@socketio.on('joined', namespace='/chat')
def emit_to_room(room: Room, message: str, data: dict | str, ommited_user: User | None) -> None:
    for usersid in room.users_sid:
        if usersid.user == ommited_user: continue
        socketio.emit(message, data, room=usersid.sid) 


@app.route("/api/new_room", methods=["POST"])
def new_room():
    room = room_manager.new_room()
    return redirect(f"/room/{room.id}")

@app.route("/")
def index():
    resp = make_response(render_template("index.html"))
    add_userid_request(resp)
    return resp

@app.route("/room/<path:id>")
def room(id):
    room = room_manager.get_room(id)
    filename = "room.html" if room else "room-404.html"

    resp = make_response(render_template(filename, room=id))
    add_userid_request(resp)

    return resp

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

if __name__ == "__main__":
    socketio.run(app)

# if __name__ == "__main__":
    # main()