import psycopg2
from config import POSTGRES_DSN

class DB:
    def __init__(self):
        self.conn = psycopg2.connect(POSTGRES_DSN)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()

    def fetchone(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()

    def fetchall(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())

db = DB()
