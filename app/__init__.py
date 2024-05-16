from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from .models import db
from .routes import api
from .swagger_bp import swagger_bp, swagger_ui_blueprint
import asyncio
from bot.bot import main

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database_name'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(swagger_bp, url_prefix='/api/docs')
    app.register_blueprint(swagger_ui_blueprint, url_prefix='/api/docs')

    return app


def create_app():
    asyncio.run(main())
