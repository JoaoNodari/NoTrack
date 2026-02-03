import psycopg2

def get_connection():
    return psycopg2.connect(
        host="172.16.0.139",
        database="Teste",
        user="joao",
        password="Peol@2016",
        port="5432"
    )
