# Running the backend with gunicorn
# gunicorn -w 4 wsgi:app
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
