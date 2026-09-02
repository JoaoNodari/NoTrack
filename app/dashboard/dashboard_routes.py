# Define as rotas HTTP relacionadas ao dashboard.
# Esta área reúne os dados financeiros e os envia para a interface.

from datetime import datetime

from flask import Blueprint, render_template, request, session

from app.auth.auth_decorators import login_required
from app.models.lancamento import total_por_categoria_no_mes, gasto_por_mes_no_ano, total_anual_por_categoria, total_credito_no_mes, total_por_forma_pagamento_no_mes, comparativo_pix_credito, resumo_do_mes

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    usuario_id = session["usuario_id"]

    hoje = datetime.now()

    mes = int(request.args.get("mes", hoje.month))
    ano = int(request.args.get("ano", hoje.year))

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