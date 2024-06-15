### Backend Application README.md

---

#### Introduction
This README file provides an overview of the backend application developed for managing employers and job seekers. The application includes features such as user registration, authentication, profile management, and email notifications.

---

#### Technologies Used
- **Python**: Programming language used for backend logic.
- **Flask**: Web framework for building the RESTful API.
- **SQLAlchemy**: SQL toolkit and ORM used for database operations.
- **MySQL**: Relational database management system for storing data.
- **JWT (JSON Web Tokens)**: Used for authentication and authorization.
- **Flask-Mail**: Extension for sending email notifications.

---

#### Project Structure
The project is organized as follows:
- **app/**
  - **__init__.py**: Initializes the Flask application and extensions.
  - **config.py**: Configuration settings including database URI, session settings, and email configuration.
  - **queries/**
    - **auth.py**: Contains functions for user authentication and registration.
    - **balance.py**: Manages employer balances and transactions.
  - **routes/**
    - **auth.py**: Defines routes for user authentication and registration.
    - **balance.py**: Defines routes for managing employer balances.
  - **static/**: Directory for static files such as CSS stylesheets.
  - **templates/**: Directory for HTML templates.

---

#### Setup Instructions
To set up the backend application locally, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Back-Munka
   pip install -r requirements.txt
3. **Database Configuration**
   ```bash
   Ensure MySQL is installed and running.
   Update the database URI in config.py with your MySQL credentials:
   SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/database_name'
   Create the necessary tables by running:
   python manage.py create_db
3. **Run the Application**
   python run.py

The application will start running at http://127.0.0.1:5000.

---

API Endpoints
- **POST** /register: Registers a new employer with email, password, full name, and phone.
- **POST** /login: Authenticates an employer using email and password.
- **POST** /logout: Logs out the currently authenticated employer.
- **GET**/profile: Retrieves the profile information of the authenticated employer.
- **POST** /send_email: Sends an email to the specified address (for password reset).

---

### Contributors
1. Vladimir (vladimir.973@list.ru)
