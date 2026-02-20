import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv # Importa a biblioteca

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()

def get_connection():
    # Agora o os.getenv vai buscar a URL de forma segura
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("ERRO: Variável DATABASE_URL não encontrada no arquivo .env")

    result = urlparse(database_url)

    return psycopg2.connect(
        host=result.hostname,
        database=result.path[1:],
        user=result.username,
        password=result.password,
        port=result.port,
        sslmode='require'
    )