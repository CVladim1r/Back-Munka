from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.routes.main import main_bp
from app.routes.auth import auth_bp

load_dotenv()

app = Flask(__name__)

app.config.from_object('app.config.Config')
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

db = SQLAlchemy(app)  # для работы с базой данных
jwt = JWTManager(app)  # для управления JWT-токенами
