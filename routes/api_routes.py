
from flask import redirect

from vars import Vars

# TODO: IMPLEMENT PERMISSIONS & OTHER API THINGS

app = Vars.app
room_manager = Vars.room_manager

@app.route("/api/new_room", methods=["POST"])
def new_room():
    room = room_manager.new_room()
    return redirect(f"/room/{room.id}")