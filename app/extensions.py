# Centraliza as extensões utilizadas pela aplicação Flask.
# Aqui são criadas integrações como SQLAlchemy e Flask-Migrate,
# que serão inicializadas pela Application Factory.

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()