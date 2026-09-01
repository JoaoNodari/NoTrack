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

@app.route("/lancamentos")
@login_required
def lancamentos():
    usuario_id = session["usuario_id"]

    mes = int(request.args.get("mes", 1))
    ano = int(request.args.get("ano", 2026))
    forma = request.args.get("forma")
    categoria_id = request.args.get("categoria_id")
    tipo = request.args.get("tipo")

    if categoria_id:
        categoria_id = int(categoria_id)

    lancamentos = listar_lancamentos_filtrados(
        usuario_id=usuario_id,
        ano=ano,
        mes=mes,
        forma_pagamento=forma,
        categoria_id=categoria_id,
        tipo=tipo
    )

    categorias = listar_categorias_por_usuario(usuario_id)

    return render_template("lancamentos.html", lancamentos=lancamentos, categorias=categorias, mes=mes, ano=ano)

@app.route("/lancamento/novo", methods=["GET", "POST"])
@login_required
def novo_lancamento():
    usuario_id = session["usuario_id"]

    if request.method == "POST":
        valor = float(request.form["valor"])
        categoria_id = int(request.form["categoria_id"])
        data = request.form["data"]
        forma_pagamento = request.form["forma_pagamento"]
        descricao = request.form.get("descricao")

        criar_lancamento(usuario_id, categoria_id, valor, data, forma_pagamento, descricao)
        return redirect(url_for("lancamentos"))

    categorias = listar_categorias_por_usuario(usuario_id)
    return render_template("novo_lancamento.html", categorias=categorias)

@app.route("/lancamento/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_lancamento(id):
    usuario_id = session["usuario_id"]

    if request.method == "POST":
        atualizar_lancamento(
            id,
            usuario_id,
            request.form["valor"],
            request.form["categoria_id"],
            request.form["data"],
            request.form["descricao"]
        )
        return redirect(url_for("lancamentos"))

    lancamento = buscar_lancamento_por_id(id, usuario_id)
    categorias = listar_categorias_por_usuario(usuario_id)
    return render_template("editar_lancamento.html", lancamento=lancamento, categorias=categorias)

@app.route("/lancamento/excluir/<int:id>")
@login_required
def excluir_lancamento_route(id):
    usuario_id = session["usuario_id"]
    excluir_lancamento(id, usuario_id)
    return redirect(url_for("lancamentos"))

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

@app.route("/lancamentos/exportar")
@login_required
def exportar_lancamentos():
    usuario_id = session["usuario_id"]

    mes = int(request.args.get("mes", 1))
    ano = int(request.args.get("ano", 2026))

    csv_content = exportar_lancamentos_csv(usuario_id, ano, mes)

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=lancamentos_{mes}_{ano}.csv"}
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=app.config["PORT"],
        debug=app.config["FLASK_DEBUG"]
    )