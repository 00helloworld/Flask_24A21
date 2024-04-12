from app import db

class FormativeAssessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment_name = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    attempts_allowed = db.Column(db.Integer, nullable=False)
    immediate_feedback = db.Column(db.Boolean, nullable=False)
