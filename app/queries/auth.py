# app/queries/auth.py
from sqlalchemy import text
from ..db_utils import get_db

def register_employer(email, password_hash, full_name, address=None, phone=None):
    db = get_db()
    try:
        # Insert employer
        db.execute(
            text("""
            INSERT INTO employers (email, password_hash)
            VALUES (:email, :password_hash)
            """),
            {'email': email, 'password_hash': password_hash}
        )
        db.commit()

        # Get employer id
        employer_id = db.execute(text("SELECT LAST_INSERT_ID()")).fetchone()[0]

        # Insert employer info
        db.execute(
            text("""
            INSERT INTO employers_info (employers_id, full_name, address, phone)
            VALUES (:employers_id, :full_name, :address, :phone)
            """),
            {'employers_id': employer_id, 'full_name': full_name, 'address': address, 'phone': phone}
        )
        db.commit()
        return True
    except Exception as e:
        print(f"Error registering employer: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def get_employer_by_email(email):
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
