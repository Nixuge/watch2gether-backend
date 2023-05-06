import routes.api_routes
import routes.html_routes
import routes.socket_routes

from data.vars import Vars

if __name__ == "__main__":
    # host=0.0.0.0 for debugging only

    # Vars.socketio.run(Vars.app, port=2135, host="0.0.0.0")
    Vars.socketio.run(Vars.app, port=2135)

#TODO:
# -SQL db w existing files
# -search for above
# -frontend (vue)
