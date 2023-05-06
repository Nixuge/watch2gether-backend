from flask_socketio import SocketIO

from flask import Flask
from room import RoomManager
from user import UserManager


class Vars:
    app = Flask(__name__)
    socketio = SocketIO(app,cors_allowed_origins="*")
    user_manager = UserManager() # Could've been made static
    room_manager = RoomManager() # same
