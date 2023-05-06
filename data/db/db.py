import sqlite3
from flask import g
from data.db.queries import CREATE_TABLE_QUERY

from data.vars import Vars

# Honestly looking kinda jank, but it's in the wiki and seems to work?
# https://flask.palletsprojects.com/en/2.3.x/patterns/sqlite3/

app = Vars.app

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('media.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# init on first load
with app.app_context():
    conn = get_db()
    conn.cursor().execute(CREATE_TABLE_QUERY)
    conn.close()
