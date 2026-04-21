from flask import Flask
from backend.models import db
from backend.auth_api import auth
from backend.ticket_api import ticket
from backend.dashboard_api import dashboard
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(ticket)
app.register_blueprint(dashboard)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)