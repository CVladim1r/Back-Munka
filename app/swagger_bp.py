from flask import Blueprint, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask import current_app as app

swagger_bp = Blueprint('swagger', __name__)

@swagger_bp.route('/swagger.json')
def swagger_json():
    return send_from_directory('static', 'swagger.json')

@swagger_bp.route('/')
def swagger_ui():
    return send_from_directory('swagger_ui', 'index.html')

@swagger_bp.route('/<path:path>')
def static_file(path):
    return send_from_directory('swagger_ui', path)

SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Employer API",
        'swagger_url': SWAGGER_URL + '/swagger.json',
    }
)
