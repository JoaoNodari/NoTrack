from flask import render_template, request, redirect, url_for, Response, session, flash
from app import create_app
from app.auth.auth_decorators import login_required
import os
from models.lancamento import (
    criar_lancamento,
    buscar_lancamento_por_id,
    atualizar_lancamento,
    excluir_lancamento,
    listar_lancamentos_filtrados,
    exportar_lancamentos_csv
)
from models.categoria import (
    listar_categorias_por_usuario,
    criar_categoria,
    atualizar_categoria,
    buscar_categoria_por_id
)

from rich.traceback import install

install()

app = create_app()

def format_brl(valor):
    try:
        return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return valor

app.jinja_env.filters["brl"] = format_brl

@app.route("/")
def home():
    return redirect(url_for("dashboard.dashboard"))

@app.route("/categoria/nova", methods=["POST"])
@login_required
def nova_categoria():
    usuario_id = session["usuario_id"]
    criar_categoria(usuario_id, request.form["nome"], request.form["tipo"])
    return redirect(url_for("categorias"))

@app.route("/categorias")
@login_required
def categorias():
    usuario_id = session["usuario_id"]
    categorias = listar_categorias_por_usuario(usuario_id)
    return render_template("categorias.html", categorias=categorias)

@app.route("/categoria/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_categoria(id):
    usuario_id = session["usuario_id"]

    if request.method == "POST":
        atualizar_categoria(id, usuario_id, request.form["nome"], request.form["tipo"])
        return redirect(url_for("categorias"))

    categoria = buscar_categoria_por_id(id, usuario_id)
    return render_template("editar_categoria.html", categoria=categoria)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=app.config["PORT"],
        debug=app.config["FLASK_DEBUG"]
    )