import os

import psycopg2
from dotenv import load_dotenv

load_dotenv() # Carrega as variáveis do arquivo .env para o sistema

def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL não configurada.")

    return psycopg2.connect(database_url)