from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.routes.main import main_bp
from app.routes.auth import auth_bp

# Вместо app.register_blueprint(main_bp) можно использовать app.register_blueprint(main_bp, url_prefix='/prefix'), если хотите добавить префикс к маршруту.

# Загрузка переменных окружения из файла .env
load_dotenv()

# Создание экземпляра приложения Flask
app = Flask(__name__)

# Загрузка конфигурации из файла config.py
app.config.from_object('app.config.Config')
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

# Инициализация расширений
db = SQLAlchemy(app)  # Инициализация SQLAlchemy для работы с базой данных
jwt = JWTManager(app)  # Инициализация JWTManager для управления JWT-токенами

# Импорт маршрутов, чтобы они были доступны приложению
from app import routes
