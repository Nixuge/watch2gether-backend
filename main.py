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

# TODO: actually delete the room after a while
# maybe another check thread like on mediagrabber ?
# (eg. note last update packet time, poll every 10s, if no updates after 10min delete)
# (same w sid requests iirc)
# to see.