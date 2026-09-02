# Ponto de entrada da aplicação NoTrack.
# Responsável por criar a aplicação Flask
# e iniciar o servidor de desenvolvimento.

from app import create_app
from rich.traceback import install

install()

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=app.config["PORT"],
        debug=app.config["FLASK_DEBUG"]
    )