from flask import Flask, render_template, request, redirect, url_for, Response, session, flash
from models.usuario import criar_usuario, validar_login
from functools import wraps
from models.lancamento import (
    total_por_categoria_no_mes,
    gasto_por_mes_no_ano,
    total_anual_por_categoria,
    criar_lancamento,
    buscar_lancamento_por_id,
    atualizar_lancamento,
    listar_lancamentos_por_mes,
    excluir_lancamento,
    total_credito_no_mes,
    total_por_forma_pagamento_no_mes,
    comparativo_pix_credito,
    resumo_do_mes,
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

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_key")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        criar_usuario(nome, email, senha)
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        user = validar_login(email, senha)

        if user:
            session.clear()
            session["usuario_id"] = user["id"]
            session["usuario_nome"] = user["nome"]
            return redirect(url_for("dashboard"))

        session.clear()
        return render_template("login.html", erro="Email ou senha inválidos")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    usuario_id = session["usuario_id"]

    mes = int(request.args.get("mes", 1))
    ano = int(request.args.get("ano", 2026))

    gastos_mes = total_por_categoria_no_mes(usuario_id, "gasto", ano, mes)
    gastos_ano = gasto_por_mes_no_ano(usuario_id, ano)
    total_categoria_ano = total_anual_por_categoria(usuario_id, "gasto", ano)
    formas_mes = total_por_forma_pagamento_no_mes(usuario_id, ano, mes)
    total_credito = total_credito_no_mes(usuario_id, ano, mes)
    pix_credito = comparativo_pix_credito(usuario_id, ano, mes)
    total_gasto, total_receita, saldo, qtd = resumo_do_mes(usuario_id, ano, mes)

    return render_template(
        "dashboard.html",
        categorias_mes=[i[0] for i in gastos_mes],
        valores_mes=[float(i[1]) for i in gastos_mes],
        meses_ano=[int(i[0]) for i in gastos_ano],
        valores_ano=[float(i[1]) for i in gastos_ano],
        formas_labels=[f[0] for f in formas_mes],
        formas_valores=[float(f[1]) for f in formas_mes],
        total_credito=total_credito,
        labels_pc=[i[0] for i in pix_credito],
        valores_pc=[float(i[1]) for i in pix_credito],
        total_gasto=total_gasto,
        total_receita=total_receita,
        saldo=saldo,
        qtd=qtd,
        mes=mes,
        ano=ano
    )

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
    app.run(debug=True)