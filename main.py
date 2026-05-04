from pathlib import Path

from flask import Flask, send_from_directory
from flask_cors import CORS

from .auth_api import auth
from .dashboard_api import dashboard
from .models import db
from .ticket_api import ticket


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


def create_app(database_uri=None):
    app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path="")
    CORS(app)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri or f"sqlite:///{BASE_DIR / 'database.db'}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(ticket)
    app.register_blueprint(dashboard)

    @app.route("/")
    def index():
        return send_from_directory(FRONTEND_DIR, "login.html")

    @app.route("/<path:filename>")
    def frontend(filename):
        return send_from_directory(FRONTEND_DIR, filename)

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
