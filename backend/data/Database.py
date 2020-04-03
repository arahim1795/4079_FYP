import psycopg2
import warnings


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def _connect(self):
        if not self.connection or self.connection.closed != 0:
            try:
                self.connection = psycopg2.connect(
                    host="localhost", database="fyp", user="postgres", password="root"
                )
                self.cursor = self.connection.cursor()
            except Exception:
                print("Unable to connect to database")

    def _disconnect(self):
        if self.connection and self.connection.closed == 0:
            self.cursor = None
            self.connection.close()

    def _execute(self, query: str):
        # handle empty query
        query = query.strip()
        if not query:
            warnings.warn("empty query")
            return

        # database actions
        self._connect()

        try:
            self.cursor.execute(query)
        except Exception as e:
            print(e)

        self._disconnect()

    def read(self, query: str) -> tuple:
        data = None

        # handle empty query
        query = query.strip()
        if not query:
            warnings.warn("empty query")
            return

        # database actions
        self._connect()

        try:
            self.cursor.execute(query)
            data = self.cursor.fetchall()
        except Exception as e:
            print(e)

        self._disconnect()

        return data

    def write(self, query: str, value: tuple):
        # handle empty query
        query = query.strip()
        if not query:
            warnings.warn("empty query")
            return

        # database actions
        self._connect()

        try:
            self.cursor.execute(query, value)
            self.connection.commit()
        except Exception as e:
            print(e)

        self._disconnect()
