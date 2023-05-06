
import sqlite3
from flask import redirect, request
from config.key_loader import get_key
from data.db.db import get_db
from data.db.queries import Queries

from data.vars import Vars

# TODO: IMPLEMENT PERMISSIONS & OTHER API THINGS

app = Vars.app
room_manager = Vars.room_manager
key = get_key()

@app.route("/api/new_room", methods=["POST"])
def new_room():
    room = room_manager.new_room()
    return redirect(f"/room/{room.id}")

@app.route("/api/add_media", methods=["POST"])
def add_media():
    content = request.json
    if content["token"] != key:
        return "Unauthorized. See https://http.cat/401.", 401
    
    filepath = content["filepath"]
    name = content["name"]
    if filepath == '' or name == '':
        return "Bad request. See https://http.cat/400.", 400

    try:
        conn = get_db()
        conn.cursor().execute(Queries.add_media, (filepath, name))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Error sending query to DB (IntegrityError), perhaps try another filename?", 400
    except Exception as e:
        return f"Error happened while adding to db: {e}", 400

    return "successfully added", 200

@app.route("/api/find_media", methods=["POST"])
def find_media():
    content = request.json
    
    search = content["search"]

    try:
        conn = get_db()
        movies = conn.cursor().execute(Queries.find_media, (search,)).fetchmany(size=10)
    except Exception as e:
        return f"Error happened while searching db: {e}", 400

    # not really needed (wasting cpu time) but clearer requests
    movies_formatted = [{"filepath": movie[0], "name": movie[1]} for movie in movies]

    return movies_formatted, 200