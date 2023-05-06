from flask import Flask
from flask_socketio import SocketIO
from data.room import RoomManager
from data.user import UserManager

import routes.api_routes
import routes.html_routes
import routes.socket_routes

from data.vars import Vars

if __name__ == "__main__":
    Vars.socketio.run(Vars.app)

# if __name__ == "__main__":
    # main()