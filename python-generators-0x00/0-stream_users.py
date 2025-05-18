import mysql.connector
from mysql.connector import Error

def stream_users():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True) 

        cursor.execute("SELECT * FROM user_data")

        for row in cursor:  
            yield row      

    except Error as e:
        print(f"❌ Database error: {e}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
