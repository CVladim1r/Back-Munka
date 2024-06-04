from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from flask_session import Session

load_dotenv()

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object('app.config.Config')
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

db = SQLAlchemy(app)
jwt = JWTManager(app)
Session(app)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
