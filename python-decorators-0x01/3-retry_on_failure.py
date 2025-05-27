import time
import sqlite3 
import functools

#### paste your with_db_decorator here

""" your code goes here"""

def with_db_connection(func):
    """ your code goes here""" 
    def wrapper(*args , **kwargs):
        conn = sqlite3.connect('users.db')
        func(conn, *args , **kwargs)
        conn.close
    return wrapper

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, retries + 1):
                try:
                    print(f"Attempt {attempt}/{retries}...")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Failed attempt {attempt}: {e}")
                    last_exception = e
                    time.sleep(delay)
            print("All attempts failed.")
            raise last_exception  # Raise the last error
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)