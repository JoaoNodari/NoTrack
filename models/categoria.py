from database.connection_local import get_connection

def listar_categorias_por_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nome, tipo
        FROM categorias
        WHERE usuario_id = %s
        ORDER BY tipo, nome
        """,
        (usuario_id,)
    )

    categorias = cursor.fetchall()

    cursor.close()
    conn.close()

    return categorias


def criar_categoria(usuario_id, nome, tipo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO categorias (usuario_id, nome, tipo)
        VALUES (%s, %s, %s)
        """,
        (usuario_id, nome, tipo)
    )

    conn.commit()
    cursor.close()
    conn.close()

def buscar_categoria_por_id(id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, tipo
        FROM categorias
        WHERE id = %s AND usuario_id = %s
    """, (id, usuario_id))

    categoria = cursor.fetchone()
    cursor.close()
    conn.close()
    return categoria

def atualizar_categoria(id, usuario_id, nome, tipo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE categorias
        SET nome = %s,
            tipo = %s
        WHERE id = %s AND usuario_id = %s
    """, (nome, tipo, id, usuario_id))

    conn.commit()
    cursor.close()
    conn.close()