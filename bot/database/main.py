import sqlite3 as sql
from sqlite3 import Connection
import os

from loguru import logger

from bot.database.methods.create import create_query

def create_connection(path: str):
    connection = None
    try:
        connection: Connection = sql.connect(path)
        logger.info('[+] Successfully connection to DB')
    except Exception as ex:
        logger.error(ex)
    return connection

connection = create_connection(os.path.join(f"{os.path.abspath(__file__)}\..",'database.db'))

create_query(connection,'''
    CREATE TABLE IF NOT EXISTS City(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(30),
        operator_link TEXT
    )
''')

create_query(connection, '''
    CREATE TABLE IF NOT EXISTS Good(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(30),
        price TEXT
    )
''')

create_query(connection, '''
    CREATE TABLE IF NOT EXISTS Stock(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_id INTEGER REFERENCES City(id) ON DELETE CASCADE,
        good_id INTEGER REFERENCES Good(id) ON DELETE CASCADE
    )
''')

create_query(connection,'''
    CREATE TABLE IF NOT EXISTS Review(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE DEFAULT current_timestamp,
        rating INTEGER,
        customer VARCHAR(30),
        review TEXT
    )
''')

create_query(connection,'''
    CREATE TABLE IF NOT EXISTS User(
        id INTEGER PRIMARY KEY,
        username VARCHAR(30),
        date DATE DEFAULT current_timestamp
    )
''')
