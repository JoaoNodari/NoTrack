from database.connection_local import get_connection
import csv
from io import StringIO

def criar_lancamento(usuario_id, categoria_id, valor, data, forma_pagamento, descricao=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO lancamentos (usuario_id, categoria_id, valor, data, forma_pagamento, descricao)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (usuario_id, categoria_id, valor, data, forma_pagamento, descricao)
    )

    conn.commit()
    cursor.close()
    conn.close()


def total_por_categoria_no_mes(usuario_id, tipo, ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.nome, COALESCE(SUM(l.valor), 0)
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
          AND c.tipo = %s
          AND EXTRACT(YEAR FROM l.data) = %s
          AND EXTRACT(MONTH FROM l.data) = %s
        GROUP BY c.nome
        ORDER BY c.nome
        """,
        (usuario_id, tipo, ano, mes)
    )

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado


def gasto_por_mes_no_ano(usuario_id, ano):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT EXTRACT(MONTH FROM l.data) AS mes, COALESCE(SUM(l.valor), 0)
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
          AND c.tipo = 'gasto'
          AND EXTRACT(YEAR FROM l.data) = %s
        GROUP BY mes
        ORDER BY mes
        """,
        (usuario_id, ano)
    )

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado


def total_anual_por_categoria(usuario_id, tipo, ano):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT c.nome, COALESCE(SUM(l.valor), 0)
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
          AND c.tipo = %s
          AND EXTRACT(YEAR FROM l.data) = %s
        GROUP BY c.nome
        ORDER BY c.nome
        """,
        (usuario_id, tipo, ano)
    )

    resultado = cursor.fetchall()

    cursor.close()
    conn.close()

    return resultado

def listar_lancamentos_por_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT l.id, l.valor, l.data, l.descricao, c.nome, c.tipo
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
        ORDER BY l.data DESC
    """, (usuario_id,))

    dados = cursor.fetchall()

    cursor.close()
    conn.close()
    return dados


def buscar_lancamento_por_id(lancamento_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, valor, categoria_id, data, descricao
        FROM lancamentos
        WHERE id = %s AND usuario_id = %s
    """, (lancamento_id, usuario_id))

    lancamento = cursor.fetchone()

    cursor.close()
    conn.close()
    return lancamento


def atualizar_lancamento(lancamento_id, usuario_id, valor, categoria_id, data, descricao):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lancamentos
        SET valor = %s,
            categoria_id = %s,
            data = %s,
            descricao = %s
        WHERE id = %s AND usuario_id = %s
    """, (valor, categoria_id, data, descricao, lancamento_id, usuario_id))

    conn.commit()
    cursor.close()
    conn.close()

def listar_lancamentos_por_mes(usuario_id, ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            l.id,
            TO_CHAR(l.data, 'YYYY-MM-DD'),
            l.valor,
            l.descricao,
            l.forma_pagamento,
            c.id,
            c.nome,
            c.tipo
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
          AND EXTRACT(YEAR FROM l.data) = %s
          AND EXTRACT(MONTH FROM l.data) = %s
        ORDER BY l.data DESC
    """, (usuario_id, ano, mes))

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    return resultado

def excluir_lancamento(lancamento_id, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM lancamentos
        WHERE id = %s AND usuario_id = %s
    """, (lancamento_id, usuario_id))

    conn.commit()
    cursor.close()
    conn.close()

def total_por_forma_pagamento_no_mes(usuario_id, ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            forma_pagamento,
            COALESCE(SUM(valor), 0)
        FROM lancamentos
        WHERE usuario_id = %s
          AND EXTRACT(YEAR FROM data) = %s
          AND EXTRACT(MONTH FROM data) = %s
        GROUP BY forma_pagamento
        ORDER BY forma_pagamento
    """, (usuario_id, ano, mes))

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    return resultado


def total_credito_no_mes(usuario_id, ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(valor), 0)
        FROM lancamentos
        WHERE usuario_id = %s
          AND forma_pagamento = 'credito'
          AND EXTRACT(YEAR FROM data) = %s
          AND EXTRACT(MONTH FROM data) = %s
    """, (usuario_id, ano, mes))

    total = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    return total

def comparativo_pix_credito(usuario_id, ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            forma_pagamento,
            COALESCE(SUM(valor), 0)
        FROM lancamentos
        WHERE usuario_id = %s
          AND forma_pagamento IN ('pix', 'credito')
          AND EXTRACT(YEAR FROM data) = %s
          AND EXTRACT(MONTH FROM data) = %s
        GROUP BY forma_pagamento
    """, (usuario_id, ano, mes))

    resultado = cursor.fetchall()
    cursor.close()
    conn.close()

    return resultado

def resumo_do_mes(usuario_id, ano, mes):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            COALESCE(SUM(CASE WHEN c.tipo = 'gasto' THEN l.valor ELSE 0 END), 0) AS total_gasto,
            COALESCE(SUM(CASE WHEN c.tipo = 'receita' THEN l.valor ELSE 0 END), 0) AS total_receita,
            COUNT(*) AS qtd_lancamentos
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
          AND EXTRACT(YEAR FROM l.data) = %s
          AND EXTRACT(MONTH FROM l.data) = %s
    """, (usuario_id, ano, mes))

    total_gasto, total_receita, qtd = cur.fetchone()
    conn.close()

    saldo = total_receita - total_gasto

    return total_gasto, total_receita, saldo, qtd

def listar_lancamentos_filtrados(usuario_id, ano, mes, forma_pagamento=None, categoria_id=None, tipo=None):
    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT l.id, l.data, l.valor, l.descricao, c.nome, c.tipo, l.forma_pagamento
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
          AND EXTRACT(YEAR FROM l.data) = %s
          AND EXTRACT(MONTH FROM l.data) = %s
    """

    params = [usuario_id, ano, mes]

    if forma_pagamento:
        query += " AND l.forma_pagamento = %s"
        params.append(forma_pagamento)

    if categoria_id:
        query += " AND l.categoria_id = %s"
        params.append(categoria_id)

    if tipo:
        query += " AND c.tipo = %s"
        params.append(tipo)

    query += " ORDER BY l.data DESC"

    cur.execute(query, params)
    dados = cur.fetchall()
    conn.close()

    return dados

def exportar_lancamentos_csv(usuario_id, ano, mes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            TO_CHAR(l.data, 'DD/MM/YYYY') as data,
            c.nome as categoria,
            c.tipo as tipo,
            l.valor,
            l.descricao,
            l.forma_pagamento
        FROM lancamentos l
        JOIN categorias c ON c.id = l.categoria_id
        WHERE l.usuario_id = %s
          AND EXTRACT(YEAR FROM l.data) = %s
          AND EXTRACT(MONTH FROM l.data) = %s
        ORDER BY l.data
    """, (usuario_id, ano, mes))

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    output = StringIO()
    writer = csv.writer(output, delimiter=';')

    writer.writerow(["Data", "Categoria", "Tipo", "Valor", "Descrição", "Forma de Pagamento"])

    for linha in dados:
        writer.writerow(linha)

    return output.getvalue()