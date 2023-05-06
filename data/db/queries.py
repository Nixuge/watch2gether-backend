class Queries:
    create_table = """CREATE TABLE IF NOT EXISTS media (
                        filepath TEXT NOT NULL,
                        name TEXT NOT NULL,

                        PRIMARY KEY (filepath)
                        );"""

    add_media = """INSERT INTO media VALUES (?, ?);"""

    find_media = """SELECT * FROM media WHERE name LIKE ?;"""