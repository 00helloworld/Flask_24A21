from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
print(Config.SQLALCHEMY_DATABASE_URI)

db = SQLAlchemy(app)

from app import routes, models


# 创建数据库表，仅在首次运行应用时创建
with app.app_context():
    db.create_all()