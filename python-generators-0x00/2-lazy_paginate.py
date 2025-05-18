import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        result = cursor.fetchall()

        return result

    except Error as e:
        print(f"❌ Error: {e}")
        return []

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass



def lazy_paginate(page_size):
    offset = 0
    while True:  # only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


for page in lazy_paginate(5):
    print("New page:")
    for user in page:
        print(user)
