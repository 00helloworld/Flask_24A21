from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    attempts = db.relationship('UserAttempt', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User ({self.username}, {self.role})>'


class UserAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,  db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.Integer,  db.ForeignKey('user.username'), nullable=False)
    assessment_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=False)
    answers = db.relationship('UserAnswer', backref='user_attempt', lazy=True)

    def __repr__(self):
        return f"UserAttempt('{self.user_id}', '{self.assessment_id}', '{self.answers}', '{self.score}', '{self.timestamp}')"

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_attempt_id = db.Column(db.Integer, db.ForeignKey('user_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option = db.Column(db.String(1), nullable=False)
    text_answer = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"UserAnswer('{self.user_attempt_id}', '{self.question_id}', '{self.selected_option}', '{self.is_correct}')"
