from flask import Blueprint, request, jsonify, session, render_template
from app.queries.auth import register_employer, get_employer_by_email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import logging

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    address = data.get('address')
    phone = data.get('phone')

    logging.info(f'Received data: email={email}, password={password}, full_name={full_name}, address={address}, phone={phone}')

    if not email or not password:
        logging.error('Email and password are required')
        return jsonify({"msg": "Email and password are required"}), 400

    password_hash = generate_password_hash(password)

    if register_employer(email, password_hash, full_name, address, phone):
        return jsonify({"msg": "Registration successful"}), 201
    else:
        logging.error('Registration failed')
        return jsonify({"msg": "Registration failed"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    logging.info(f'Received data: email={email}, password={password}')

    if not email or not password:
        logging.error('Email and password are required')
        return jsonify({"msg": "Email and password are required"}), 400

    employer = get_employer_by_email(email)

    if employer and check_password_hash(employer.password_hash, password):
        session['user_id'] = employer.id
        return jsonify({"msg": "Login successful"}), 200
    else:
        logging.error('Invalid email or password')
        return jsonify({"msg": "Invalid email or password"}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"msg": "Logout successful"}), 200

@auth_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        # Get user details using user_id
        return jsonify({"user_id": user_id}), 200
    else:
        return jsonify({"msg": "Unauthorized"}), 401

@auth_bp.route('/verify_token', methods=['POST'])
@jwt_required()
def verify_token():
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        return jsonify({'msg': 'Token is valid', 'user': current_user}), 200
    except Exception as e:
        return jsonify({'msg': 'Token is invalid', 'error': str(e)}), 401

