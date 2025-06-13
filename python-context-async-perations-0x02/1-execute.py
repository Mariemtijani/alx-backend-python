#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    def __init__(self, db_file, query, params=None):
        self.db_file = db_file
        self.query = query
        self.params = params if params is not None else ()
        self.connection = None
        self.result = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_file)
        cursor = self.connection.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    db_file = "my_database.db"  # replace with your database
    query = "SELECT * FROM users WHERE age > ?"
    param = (25, )

    with ExecuteQuery(db_file, query, param) as result:
        for row in result:
            print(row)
