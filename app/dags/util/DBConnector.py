from dags.util import Singleton
import psycopg2


@Singleton
class DBConnector:
    def __init__(self, db_provider, username, password, host, port, db):
        self._db_provider = db_provider
        self._username = username
        self._password = password
        self._host = host
        self._port = port
        self._db = db

    def get_conn(self):
        connection_str: str = f"{self._db_provider}://{self._username}:{self._password}@{self._host}/{self._db}"
        with psycopg2.connect(connection_str) as conn:
            return conn
