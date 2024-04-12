from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'), nullable=False)


class UserAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Float, nullable=False)
    answers = db.relationship('UserAnswer', backref='user_attempt', lazy=True)

    def __repr__(self):
        return f"UserAttempt('{self.user_id}', '{self.assessment_id}', '{self.score}', '{self.timestamp}')"

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_attempt_id = db.Column(db.Integer, db.ForeignKey('user_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    selected_option = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"UserAnswer('{self.user_attempt_id}', '{self.question_id}', '{self.selected_option}', '{self.is_correct}')"
