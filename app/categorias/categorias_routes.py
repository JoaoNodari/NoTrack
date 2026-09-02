# Define as rotas HTTP relacionadas às categorias financeiras.
# Este arquivo recebe as requisições do usuário e coordena
# operações como listar, cadastrar e editar categorias.

from flask import render_template, request, redirect, url_for, session, Blueprint

from app.auth.auth_decorators import login_required
from app.models.categoria import listar_categorias_por_usuario, criar_categoria, atualizar_categoria, buscar_categoria_por_id

categorias_bp = Blueprint("categorias", __name__)

@categorias_bp.route("/categoria/nova", methods=["POST"])
@login_required
def nova_categoria():
    usuario_id = session["usuario_id"]
    criar_categoria(usuario_id, request.form["nome"], request.form["tipo"])
    return redirect(url_for("categorias"))

@categorias_bp.route("/categorias")
@login_required
def categorias():
    usuario_id = session["usuario_id"]
    categorias = listar_categorias_por_usuario(usuario_id)
    return render_template("categorias.html", categorias=categorias)

@categorias_bp.route("/categoria/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_categoria(id):
    usuario_id = session["usuario_id"]

    if request.method == "POST":
        atualizar_categoria(id, usuario_id, request.form["nome"], request.form["tipo"])
        return redirect(url_for("categorias"))

    categoria = buscar_categoria_por_id(id, usuario_id)
    return render_template("editar_categoria.html", categoria=categoria)