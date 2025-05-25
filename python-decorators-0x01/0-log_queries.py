import sqlite3
import functools

#### decorator to lof SQL queries

""" YOUR CODE GOES HERE"""

def log_queries(func):
    def wrapper(*args, **kwargs):
       print (f"Start execute : {func.__name__}")
       func(*args, **kwargs)
       print("Done")
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")