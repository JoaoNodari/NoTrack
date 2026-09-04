# Responsável pelo histórico de avaliações dos bens patrimoniais.
# Cada registro armazena o valor estimado de um bem em uma determinada data.

from datetime import datetime, timezone
from app.extensions import db

class HistoricoBem(db.Model):
    __tablename__ = "historico_bens"

    id = db.Column(db.Integer, primary_key=True)
    bem_id = db.Column(db.Integer, db.ForeignKey("bens.id"), nullable=False)

    valor = db.Column(db.Numeric(12, 2), nullable=False)
    data_referencia = db.Column(db.Date, nullable=False)

    criado_em = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=db.func.now()
    )
    
    __table_args__ = (
        db.CheckConstraint(
            "valor >= 0",
            name="ck_historico_bens_valor"
        ),

        db.UniqueConstraint(
            "bem_id",
            "data_referencia",
            name="uq_historico_bens_bem_data"
        ),
    )