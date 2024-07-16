from app import app  # Import the Flask application from app.py

# No need to call app() here, it's already an application object

if __name__ == '__main__':
    import gunicorn  # Assuming you're using Gunicorn as your WSGI server

    gunicorn.main() 
