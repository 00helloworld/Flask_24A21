from flask import Blueprint

bp = Blueprint('routes', __name__)

from app.routes import auth_routes, teacher_routes, student_routes