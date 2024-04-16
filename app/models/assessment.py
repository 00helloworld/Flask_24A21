from app import db

import datetime

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    type = db.Column(db.String(255), nullable=False)
    questions = db.relationship('Question', secondary='assessment_question', backref='assessments')
    parameters = db.Column(db.JSON, nullable=True)

class AssessmentQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


# class AssessmentAttempt(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_attempt_id = db.Column(db.Integer, db.ForeignKey('user_attempt.id'), nullable=False)
#     assessment_id = db.Column(db.Integer, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
#     score = db.Column(db.Float, nullable=False)
#     answers = db.Column(db.JSON, nullable=False)  # Storing answers as JSON

#     def __repr__(self):
#         return f"AssessmentAttempt('{self.user_attempt_id}', '{self.assessment_id}', '{self.score}', '{self.timestamp}')"

