import psycopg2
import warnings


class Db:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost", database="fyp", user="postgres", password="root"
            )
        except Exception:
            print("Unable to connect to database")

    def disconnect(self):
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def execute(self, query: str, value: tuple = None, return_data: bool = False):
        data = None

        # handle empty query
        query = query.strip()
        if not query:
            warnings.warn("empty query")
            return

        # connect to db
        if not self.connection or self.connection.closed != 0:
            self.connect()

        # execute query
        cursor = self.connection.cursor()
        if value:
            cursor.execute(query, value)
        else:
            cursor.execute(query)

        if return_data:
            data = cursor.fetchall()

        # disconnect from db
        if self.connection.closed == 0:
            self.disconnect()

        return data
