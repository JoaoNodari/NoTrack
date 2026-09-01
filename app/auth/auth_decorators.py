# Contém decorators relacionados à autenticação.
# O login_required protege rotas que só podem ser acessadas
# por usuários autenticados.

from functools import wraps

from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("auth.login"))

        return f(*args, **kwargs)

    return decorated_function