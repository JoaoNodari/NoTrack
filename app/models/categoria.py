# Responsável pela representação e acesso aos dados das categorias.
# Durante a migração para SQLAlchemy, este arquivo mantém
# temporariamente o model e as funções antigas de acesso ao banco.

from datetime import datetime, timezone
from app.extensions import db

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    nome = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True, server_default=db.true())
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), server_default=db.func.now(), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.CheckConstraint(
            "tipo IN ('receita', 'gasto', 'investimento', 'resgate')",
            name="ck_categorias_tipo"
        ),

        db.UniqueConstraint(
            "id",
            "usuario_id",
            name="uq_categorias_id_usuario"
        ),
    )

from app.database.connection import get_connection

def listar_categorias_por_usuario(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nome, tipo FROM categorias
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