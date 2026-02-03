from database.connection import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

def criar_usuario(nome, email, senha):
    conn = get_connection()
    cursor = conn.cursor()

    senha_hash = generate_password_hash(senha)

    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha_hash)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (nome, email, senha_hash))

    user_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()

    return user_id


def buscar_usuario_por_email(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, email, senha_hash
        FROM usuarios
        WHERE email = %s
    """, (email,))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    return user


def validar_login(email, senha):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, senha_hash FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return None

    if check_password_hash(user[2], senha):
        return {
            "id": user[0],
            "nome": user[1]
        }

    return None