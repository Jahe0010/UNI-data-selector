import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def connect():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        port=os.getenv('DB_PORT'),
        database="afim",
        password=os.getenv('DB_PASSWORD')
    )
    return connection