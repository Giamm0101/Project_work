import mysql.connector
from mysql.connector import Error


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, name):
    cursor = connection.cursor()
    try:
        query = f'CREATE DATABASE {name}'
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def execute_query_place(connection, query, place):
    cursor = connection.cursor()
    try:
        cursor.execute(query, place)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def execute_query_place2(connection, query, place):
    cursor = connection.cursor()
    try:
        cursor.execute(query, place)
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query, /,*,dictionary= False):
    if dictionary:
        cursor = connection.cursor(dictionary=True)
    else:
        connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def read_query_place(connection, query, place, /,*,dictionary= False):
    if dictionary:
        cursor = connection.cursor(dictionary=True)
    else:
        connection.cursor()
    result = None
    try:
        cursor.execute(query, place)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query_place1(connection, query, params):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Funzione per eseguire una query di inserimento nel database
def execute_query_place1(connection, query, params):
    try:
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def execute_query_place_many(connection, query, place, lista):
    cursor = connection.cursor()
    try:
        cursor.executemany(query, lista)
        connection.commit()
        # print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")