# Responsável pela representação dos bens que compõem o patrimônio do usuário.
# Cada bem representa um ativo patrimonial, como imóvel, veículo, joia ou outro item de valor.

from datetime import datetime, timezone
from app.extensions import db

class Bem(db.Model):
    __tablename__ = "bens"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    nome = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)
    descricao = db.Column(db.Text)
    valor_aquisicao = db.Column(db.Numeric(12, 2))
    data_aquisicao = db.Column(db.Date)

    ativo = db.Column(db.Boolean, nullable=False, default=True, server_default=db.true())
    criado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), server_default=db.func.now())
    atualizado_em = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), server_default=db.func.now(), onupdate=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        db.CheckConstraint(
            "tipo IN ('imovel', 'veiculo', 'joia', 'eletronico', 'colecionavel', 'outro')",
            name="ck_bens_tipo"
        ),
    )