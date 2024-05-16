from flask import Flask, Blueprint, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///munka.db'
db = SQLAlchemy(app)

# Определение моделей Employer и JobVacancy

api = Blueprint('api', __name__)

@api.route('/employers', methods=['POST'])
def create_employer():
    data = request.json
    new_employer = Employer(name=data['name'], email=data['email'], password=data['password'])
    try:
        db.session.add(new_employer)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Email already exists'}), 400
    return jsonify({'message': 'Employer created successfully'}), 201

@api.route('/job_vacancies', methods=['POST'])
def create_job_vacancy():
    data = request.json
    new_job_vacancy = JobVacancy(employer_id=data['employer_id'], title=data['title'], description=data['description'])
    db.session.add(new_job_vacancy)
    db.session.commit()
    return jsonify({'message': 'Job vacancy created successfully'}), 201

@api.route('/hello')
def hello():
    return {'message': 'Hello from Flask API'}

app.register_blueprint(api, url_prefix='/api')

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

app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True)
