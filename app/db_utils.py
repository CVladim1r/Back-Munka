# app/db_utils.py
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

def get_db():
    engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    db = Session()
    return db

    db = get_db()
    try:
        result = db.execute(
            text("""
            SELECT * FROM employers
            WHERE email = :email
            """),
            {'email': email}
        ).fetchone()
        return result
    except Exception as e:
        print(f"Error getting employer by email: {e}")
        return None
    finally:
        db.close()