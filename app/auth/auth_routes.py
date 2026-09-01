# Define as rotas HTTP relacionadas à autenticação,
# como cadastro, login e logout do usuário.

from flask import Blueprint, render_template, request, redirect, url_for, session

from models.usuario import criar_usuario, validar_login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        criar_usuario(nome, email, senha)

        return redirect(url_for("auth.login"))

    return render_template("auth.register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        user = validar_login(email, senha)

        if user:
            session.clear()
            session["usuario_id"] = user["id"]
            session["usuario_nome"] = user["nome"]

            return redirect(url_for("dashboard.dashboard"))

        session.clear()

        return render_template(
            "auth.login.html",
            erro="Email ou senha inválidos"
        )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("auth.login"))