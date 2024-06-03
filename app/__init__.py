# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app)
jwt = JWTManager(app)

from app import routes
