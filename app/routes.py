from flask import Blueprint, jsonify, request
from .models import db, Employer, JobVacancy
from sqlalchemy.exc import IntegrityError

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

@api.route('/api/hello')
def hello():
    return {'message': 'Hello from Flask API'}
