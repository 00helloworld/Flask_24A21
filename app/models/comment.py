from app import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(200))
    parent_comment_id = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, nullable=False)
