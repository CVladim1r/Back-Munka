# app/config.py
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SESSION_TYPE='filesystem'
    SESSION_PERMANENT=False
    SESSION_USE_SIGNER=True
    SESSION_COOKIE_HTTPONLY=True
    SESSION_COOKIE_SAMESITE='Lax'
    SECRET_KEY=os.getenv('nguiasbbiug4o3hhhouhaiu3')
    SQLALCHEMY_DATABASE_URI=os.getenv('mysql+pymysql://root:q1q1q1q1@localhost/munkaDB')
    JWT_SECRET_KEY=os.getenv('nguiasbbiug4o3hhhouhaiu2')

    MAIL_SERVER = 'smtp.mail.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'munka.help@mail.ru'
    MAIL_PASSWORD = 'EDLCw1snaCCrvJwNjqfF'
    MAIL_DEFAULT_SENDER = 'munka.help@mail.ru'