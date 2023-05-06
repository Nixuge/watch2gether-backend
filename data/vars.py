from flask_socketio import SocketIO

from flask import Flask
from data.room import RoomManager
from data.user import UserManager


class Vars:
    app = Flask(__name__, static_folder="../static", template_folder="../templates")
    socketio = SocketIO(app,cors_allowed_origins="*")
    user_manager = UserManager() # Could've been made static
    room_manager = RoomManager() # same
