
from flask import make_response, render_template, request
from data.user import User
from data.vars import Vars

# Unwrapping values for easier use
app = Vars.app
user_manager = Vars.user_manager
room_manager = Vars.room_manager

def add_userid_request(resp) -> User:
    user_id = request.cookies.get("user_id")
    user = None
    if user_id:
        user = user_manager.get_user_from_userid(user_id)
    if not user or not user_id:
        user = user_manager.new_user()
        resp.set_cookie("user_id", user.id, path="/")


@app.route("/")
def index():
    resp = make_response(render_template("index.html"))
    add_userid_request(resp)
    return resp

@app.route("/room/<path:id>")
def room(id):
    room = room_manager.get_room(id)
    filename = "room.html" if room else "room-404.html"

    resp = make_response(render_template(filename, room=id))
    add_userid_request(resp)

    return resp

@app.route("/admin/")
def admin():
    return render_template("admin.html")