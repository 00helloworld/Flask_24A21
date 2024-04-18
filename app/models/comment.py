from app import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(255), nullable=False)
    user_role = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    image = db.Column(db.String(255), nullable=True)  # 存储图片路径

    user = db.relationship('User', backref='comments', lazy=True)
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)


    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'user_id': self.user_id,
    #         'user_name': self.user_name,
    #         'user_role': self.user_role,
    #         'content': self.content,
    #         'image': self.image,
    #         'parent_id': self.parent_id,
    #         'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
    #         'username': self.user.username if self.user else None,
    #         'parent_content': self.parent_comment.content if self.parent_comment else None
    #     }

    def __repr__(self):
        return f"Comment('{self.user_id}', '{self.content}', '{self.image}', '{self.timestamp}')"