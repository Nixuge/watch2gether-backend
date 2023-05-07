class Queries:
    create_table = """CREATE TABLE IF NOT EXISTS media (
                        filepath TEXT NOT NULL,
                        name TEXT NOT NULL,
                        thumbnail TEXT,
                        tmdb_id TEXT,
                        imdb_id TEXT,

                        PRIMARY KEY (filepath)
                        );"""

    add_media = """INSERT INTO media VALUES (?, ?, ?, ?, ?);""" # TEMPORARY, NOT YET IMPLEMENTED

    find_media = """SELECT * FROM media WHERE name LIKE %?%;"""

    all_media = """SELECT * FROM media;"""