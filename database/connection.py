import os
import psycopg2

def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL, sslmode="require")

    return psycopg2.connect(
        dbname="notrack",
        user="postgres",
        password="123",
        host="localhost"
    )