import sqlite3 
import functools

"""your code goes here"""

def with_db_connection(func):
    """ your code goes here""" 
    def wrapper(*args , **kwargs):
        conn = sqlite3.connect('users.db')
        func(conn, *args , **kwargs)
        conn.close
    return wrapper

def transactional(func):
    def wrapper(conn, *arg, **kwargs):
        try :
            func(conn,*arg, **kwargs)
            conn.commit()
            print("commited")
        except Exception as e:
            conn.rollback()
            print('Transaction faild', e)
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE userId = ?", (new_email, user_id)) 
#### Update user's email with automatic transaction handling 

update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')