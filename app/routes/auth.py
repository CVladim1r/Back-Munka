from flask import Blueprint, request, jsonify, session, render_template
from app.queries.auth import register_employer, get_employer_by_email, employer_exists, update_password
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
import logging
import os
import base64
import random
from flask_mail import Message
from flask import current_app as app

# Генерация соли для хеширования паролей
def generate_salt():
    return base64.b64encode(os.urandom(16)).decode('utf-8')

# Инициализация Blueprint
auth_bp = Blueprint('auth', __name__)
logging.basicConfig(level=logging.INFO)

# Маршрут для регистрации
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

    salt = generate_salt()
    password_hash = generate_password_hash(password + salt)

    if employer_exists(email):
        logging.error('User with this email already exists')
        return jsonify({"msg": "User with this email already exists"}), 400

    try:
        if register_employer(email, password_hash, full_name, address, phone, salt):
            return jsonify({"msg": "Registration successful"}), 201
        else:
            logging.error('Registration failed')
            return jsonify({"msg": "Registration failed"}), 500
    except Exception as e:
        logging.error(f"Error registering employer: {e}")
        return jsonify({"msg": "Registration failed"}), 500

# Маршрут для входа в систему
@auth_bp.route('/login', methods=['POST'])
def login():
    logging.info(f'Headers: {request.headers}')
    logging.info(f'Is JSON: {request.is_json}')

    if request.is_json:
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
    else:
        return jsonify({"msg": "Content-Type must be application/json"}), 415

# Маршрут для выхода из системы
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({"msg": "Logout successful"}), 200

# Маршрут для получения профиля пользователя
@auth_bp.route('/profile', methods=['GET'])
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        # Здесь нужно получить детали пользователя по user_id
        return jsonify({"user_id": user_id}), 200
    else:
        return jsonify({"msg": "Access denied: unauthorized"}), 401

# Маршрут для проверки токена
@auth_bp.route('/verify_token', methods=['POST'])
@jwt_required()
def verify_token():
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        return jsonify({'msg': 'Token is valid', 'user': current_user}), 200
    except Exception as e:
        return jsonify({'msg': 'Token is invalid', 'error': str(e)}), 401

# Генерация кода для сброса пароля
def generate_reset_code():
    return str(random.randint(10000000, 99999999))

# Маршрут для отправки email
@auth_bp.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')

    # Здесь нужно добавить логику для обновления пароля пользователя в базе данных

    msg = Message(
        'Password Reset Request',
        recipients=[email],
        body=f'Hello, you requested a password reset. Your new password is: {new_password}'
    )
    app.mail.send(msg)
    return jsonify({"msg": "Email sent successfully!"}), 200

