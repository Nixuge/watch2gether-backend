#!/bin/python3
# import routes.html_routes

import routes.api_routes
import routes.socket.joinRoom
import routes.socket.playPause
import routes.socket.setVideo
import routes.socket.updateTime
import routes.socket.videoData

from data.vars import Vars

if __name__ == "__main__":
    # host=0.0.0.0 for debugging only

    # Vars.socketio.run(Vars.app, port=2135, host="0.0.0.0")
    print("Starting webserver")
    Vars.socketio.run(Vars.app, port=2135)
