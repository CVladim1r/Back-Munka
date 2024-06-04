from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
            )
        )
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.remove()
