import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import subprocess


def main():
    db_name = "fyp"

    conn = psycopg2.connect(user="postgres", password="root")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    cur = conn.cursor()

    # check if database exist
    cur.execute(
        """ SELECT 1
            FROM pg_catalog.pg_database
            WHERE datname = %s
        """,
        (db_name,),
    )
    exists = cur.fetchone()

    # create database if not exist
    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        subprocess.call([r".\backend\data\setup\setup_data.bat"])
        print("Database Created")


if __name__ == "__main__":
    main()
