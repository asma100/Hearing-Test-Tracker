from app import app

if __name__ == '__main__':
    from app import db
with app.app_context():
    db.create_all()
    app.run(debug=True)

