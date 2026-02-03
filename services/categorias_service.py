from models.categoria import criar_categoria

def criar_categoria_para_usuario(usuario_id, nome, tipo):
    if tipo not in ["receita", "gasto"]:
        raise ValueError("Tipo de categoria inválido")

    return criar_categoria(usuario_id, nome, tipo)
