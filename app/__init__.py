from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from app.routes.main import main_bp
from app.routes.auth import auth_bp
from flask_session import Session
from flask_mail import Mail, Message

load_dotenv()

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config.from_object('app.config.Config')
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

app.config['MAIL_SERVER'] = 'smtp.mail.ru'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'munka.help@mail.ru'
app.config['MAIL_PASSWORD'] = 'EDLCw1snaCCrvJwNjqfF'  
app.config['MAIL_DEFAULT_SENDER'] = 'munka.help@mail.ru'



mail = Mail(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)
Session(app)
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
