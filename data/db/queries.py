CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS media (
                    filepath TEXT NOT NULL,
                    name TEXT NOT NULL,

                    PRIMARY KEY (filepath)
                    );"""

def get_add_media_query(filepath: str, name: str):
    return f"""INSERT INTO media VALUES ('{filepath}', '{name}');"""