from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from flask_session import Session
from flask_mail import Mail

load_dotenv()

app = Flask(__name__)
app.config.from_object('app.config.Config') 

# Инициализация расширений
db = SQLAlchemy(app)
jwt = JWTManager(app)
Session(app)
CORS(app)
mail = Mail(app)

# Регистрация blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)
