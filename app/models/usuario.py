# Responsável pela representação e acesso aos dados dos usuários.
# Durante a migração para SQLAlchemy, este arquivo pode conter
# temporariamente o model e funções antigas de acesso ao banco.

from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
class Usuario(db.Model): # Significa que essa classe representa uma tabela do banco | db.Model vem do SQLAlchemy, le transforma a classe Python em algo que o SQLAlchemy consegue relacionar com uma tabela.
    __tablename__ = "usuarios" # Direciona a tabela necessária

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha_hash = db.Column(db.Text, nullable=False)
    ativo = db.Column(db.Boolean, nullable=False, default=True, server_default=db.true())
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), server_default=db.func.now(), onupdate=lambda: datetime.now(timezone.utc))
