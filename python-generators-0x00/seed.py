import mysql.connector
import pandas as pd
from mysql.connector import Error
import uuid

def connect_db():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        )
    return connection


def create_database(connection):
    cursor = connection.cursor()
    cursor.exexute(f"CREATE DATABASE IF NOT EXIST alx_prodev")
 
    
def connect_to_prodev():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "",
        database = "alx_prodev"
        )
    return connection

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(f""" CREATE TABLE IF NOT EXIST USER (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
        )"""
    )
    connection.commit()
    cursor.close()

def insert_data(connection, csv_file):
    df = pd.read_csv(csv_file)
    cursor = connection.cursor()

    insert_sql = f"""
        INSERT INTO user(user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
    """

    data = [
        (str(uuid.uuid4()), row['name'], row['email'], row['age'])
        for _, row in df.iterrows()
    ]

    cursor.executemany(insert_sql, data)
    connection.commit()
    cursor.close()