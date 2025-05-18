import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )

        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")

        for (age,) in cursor:  
            yield float(age)  
    except Error as e:
        print(f"Database error: {e}")
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

def compute_average_age():
    total_age = 0
    count = 0

    for age in stream_user_ages():  
        total_age += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total_age / count:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    compute_average_age()
