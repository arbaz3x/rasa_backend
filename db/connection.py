# db/connection.py
import psycopg2

DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rasa_db"
DB_USER = "postgres"
DB_PASSWORD = "arbaz123"

def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
