# Responsável por criar e configurar a aplicação Flask.
# A função create_app() centraliza a inicialização do sistema
# e permite registrar configurações, Blueprints e extensões em um único lugar.

from flask import Flask

from config import Config

# Importação das Blueprints
from app.auth.auth_routes import auth_bp
from app.dashboard.dashboard_routes import dashboard_bp
from app.lancamentos.lancamentos_routes import lancamentos_bp

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")

    app.config.from_object(Config)

    # Registando as blueprints da aplicação
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(lancamentos_bp)

    return app