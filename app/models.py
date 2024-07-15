from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    test_results = db.relationship('TestResult', backref='user', lazy=True)
    left_test = db.relationship('LTestvalue', backref='user', lazy=True, uselist=False)
    right_test = db.relationship('RTestvalue', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class RTestvalue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f250db = db.Column(db.Float)
    f500db = db.Column(db.Float)
    f1000db = db.Column(db.Float)
    f2000db = db.Column(db.Float)
    f4000db = db.Column(db.Float)
    f8000db = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class LTestvalue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    f250db = db.Column(db.Float)
    f500db = db.Column(db.Float)
    f1000db = db.Column(db.Float)
    f2000db = db.Column(db.Float)
    f4000db = db.Column(db.Float)
    f8000db = db.Column(db.Float)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ear = db.Column(db.String(20))
    f250db = db.Column(db.String(50))  
    f500db = db.Column(db.String(50))  
    f1000db = db.Column(db.String(50))  
    f2000db = db.Column(db.String(50))  
    f4000db = db.Column(db.String(50))  
    f8000db = db.Column(db.String(50)) 
    overall_assessment = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"TestResult('{self.ear}', '{self.date}')"


# Other parts of the code remain the same...




