# Responsável por criar e configurar a aplicação Flask.
# A função create_app() centraliza a inicialização do sistema
# e permite registrar configurações, Blueprints e extensões em um único lugar.

from flask import Flask

from config import Config

# Importação das Blueprints
from app.auth.auth_routes import auth_bp
from app.dashboard.dashboard_routes import dashboard_bp
from app.lancamentos.lancamentos_routes import lancamentos_bp
from app.main.main_routes import main_bp
from app.categorias.categorias_routes import categorias_bp

# Importando os bancos
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.models.lancamento import Lancamento
from app.models.bem import Bem
from app.models.historico_bem import HistoricoBem

from app.extensions import db, migrate

from app.utils.filters import register_filters

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Utils
    register_filters(app)

    # Registando as blueprints da aplicação
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(lancamentos_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(categorias_bp)

    return app