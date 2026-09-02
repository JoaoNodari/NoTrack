# Contém filtros personalizados utilizados nos templates Jinja.
# Esses filtros formatam dados antes de serem exibidos
# nas páginas HTML do NoTrack.


def format_brl(valor):
    try:
        return (
            f"{float(valor):,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    except (TypeError, ValueError):
        return valor


def register_filters(app):
    app.jinja_env.filters["brl"] = format_brl