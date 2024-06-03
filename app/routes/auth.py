from flask import Blueprint, request, jsonify, render_template
from app.queries.auth import register_employer, get_employer_by_email
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def index():
    return render_template('index.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    address = request.form.get('address')
    phone = request.form.get('phone')

    password_hash = generate_password_hash(password)

    if register_employer(email, password_hash, full_name, address, phone):
        return jsonify({"msg": "Registration successful"}), 201
    else:
        return jsonify({"msg": "Registration failed"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    employer = get_employer_by_email(email)

    if employer and check_password_hash(employer.password_hash, password):
        # Implement JWT authentication here
        return jsonify({"msg": "Login successful"}), 200
    else:
        return jsonify({"msg": "Invalid email or password"}), 401
