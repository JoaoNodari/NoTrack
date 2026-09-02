# Define as rotas HTTP relacionadas aos lançamentos financeiros.
# Este arquivo recebe as requisições do usuário e coordena
# operações como listar, cadastrar, editar, excluir e exportar lançamentos.

from datetime import datetime
from flask import Blueprint, Response, redirect, render_template, request, session, url_for

from app.auth.auth_decorators import login_required

from app.models.categoria import listar_categorias_por_usuario
from app.models.lancamento import atualizar_lancamento, buscar_lancamento_por_id, criar_lancamento, excluir_lancamento, exportar_lancamentos_csv, listar_lancamentos_filtrados

lancamentos_bp = Blueprint("lancamentos", __name__)

@lancamentos_bp.route("/lancamentos")
@login_required
def lancamentos():
    usuario_id = session["usuario_id"]

    hoje = datetime.now()

    mes = int(request.args.get("mes", hoje.month))
    ano = int(request.args.get("ano", hoje.year))

    forma = request.args.get("forma")
    categoria_id = request.args.get("categoria_id")
    tipo = request.args.get("tipo")

    if categoria_id:
        categoria_id = int(categoria_id)

    lista_lancamentos = listar_lancamentos_filtrados(
        usuario_id=usuario_id,
        ano=ano,
        mes=mes,
        forma_pagamento=forma,
        categoria_id=categoria_id,
        tipo=tipo
    )

    categorias = listar_categorias_por_usuario(usuario_id)

    return render_template(
        "lancamentos.html",
        lancamentos=lista_lancamentos,
        categorias=categorias,
        mes=mes,
        ano=ano,
        forma=forma,
        categoria_id=categoria_id,
        tipo=tipo
    )


@lancamentos_bp.route("/lancamento/novo", methods=["GET", "POST"])
@login_required
def novo_lancamento():
    usuario_id = session["usuario_id"]

    if request.method == "POST":
        valor = float(request.form["valor"])
        categoria_id = int(request.form["categoria_id"])
        data = request.form["data"]
        forma_pagamento = request.form["forma_pagamento"]
        descricao = request.form.get("descricao")

        criar_lancamento(
            usuario_id,
            categoria_id,
            valor,
            data,
            forma_pagamento,
            descricao
        )

        return redirect(url_for("lancamentos.lancamentos"))

    categorias = listar_categorias_por_usuario(usuario_id)

    return render_template(
        "novo_lancamento.html",
        categorias=categorias
    )


@lancamentos_bp.route(
    "/lancamento/editar/<int:id>",
    methods=["GET", "POST"]
)
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

        return redirect(url_for("lancamentos.lancamentos"))

    lancamento = buscar_lancamento_por_id(
        id,
        usuario_id
    )

    categorias = listar_categorias_por_usuario(
        usuario_id
    )

    return render_template(
        "lancamentos.editar_lancamento.html",
        lancamento=lancamento,
        categorias=categorias
    )


@lancamentos_bp.route(
    "/lancamento/excluir/<int:id>",
    methods=["POST"]
)
@login_required
def excluir_lancamento_route(id):
    usuario_id = session["usuario_id"]

    excluir_lancamento(
        id,
        usuario_id
    )

    return redirect(
        url_for("lancamentos.lancamentos")
    )


@lancamentos_bp.route("/lancamentos/exportar")
@login_required
def exportar_lancamentos():
    usuario_id = session["usuario_id"]

    hoje = datetime.now()

    mes = int(request.args.get("mes", hoje.month))
    ano = int(request.args.get("ano", hoje.year))

    csv_content = exportar_lancamentos_csv(
        usuario_id,
        ano,
        mes
    )

    return Response(
        csv_content,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename=lancamentos_{mes}_{ano}.csv"
        }
    )