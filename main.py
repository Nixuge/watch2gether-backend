from flask import Flask
from flask_socketio import SocketIO
from room import RoomManager
from user import UserManager

import routes.api_routes
import routes.html_routes
import routes.socket_routes

from vars import Vars

if __name__ == "__main__":
    Vars.socketio.run(Vars.app)

# if __name__ == "__main__":
    # main()