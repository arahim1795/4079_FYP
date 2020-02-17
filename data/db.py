import psycopg2


def db_connect():
    con, cur = None, None

    try:
        con = psycopg2.connect(
            host="localhost", database="fyp", user="postgres", password="root"
        )
    except Exception:
        con = None
        print("Unable to connect to database")

    if con is not None:
        cur = con.cursor()

    return con, cur


def db_disconnect(con):
    con.close()
