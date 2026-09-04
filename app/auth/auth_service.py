# Centraliza as regras e operações relacionadas à autenticação.
# Faz a comunicação entre as rotas de autenticação e o model Usuario.

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models.usuario import Usuario


def criar_usuario(nome, email, senha):
    senha_hash = generate_password_hash(senha)

    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash
    )

    try:
        db.session.add(usuario)
        db.session.commit()

        return {
            "sucesso": True,
            "usuario_id": usuario.id
        }

    except IntegrityError:
        db.session.rollback()

        return {
            "sucesso": False,
            "erro": "email_ja_cadastrado"
        }

    except SQLAlchemyError:
        db.session.rollback()
        raise


def validar_login(email, senha):
    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return None

    if not usuario.ativo:
        return None

    if not check_password_hash(
        usuario.senha_hash,
        senha
    ):
        return None

    return {
        "id": usuario.id,
        "nome": usuario.nome
    }