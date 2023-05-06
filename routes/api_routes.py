
from flask import redirect, request
from config.key_loader import get_key
from data.db.db import get_db
from data.db.queries import get_add_media_query

from data.vars import Vars

# TODO: IMPLEMENT PERMISSIONS & OTHER API THINGS

app = Vars.app
room_manager = Vars.room_manager
key = get_key()

@app.route("/api/new_room", methods=["POST"])
def new_room():
    room = room_manager.new_room()
    return redirect(f"/room/{room.id}")

@app.route("/api/add_movie", methods=["POST"])
def add_movie():
    content = request.json
    if content["token"] != key:
        return "Unauthorized. See https://http.cat/401.", 401
    
    filepath = content["filepath"]
    name = content["name"]
    if filepath == '' or name == '':
        return "Bad request. See https://http.cat/400.", 400

    conn = get_db()
    conn.cursor().execute(get_add_media_query(filepath, name))
    conn.commit()

    return "successfully added", 200