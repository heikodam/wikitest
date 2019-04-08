import psycopg2


def get_db():
    connection = psycopg2.connect(
        host = "localhost",
        database = "wikiCheat",
        user = "postgres",
        password = "HDamaske",
        port = 5432
    )
    connection.autocommit=True

    cursor = connection.cursor()
    return cursor

# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

# connection.close()