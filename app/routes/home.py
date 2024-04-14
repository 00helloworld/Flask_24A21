from flask import render_template, request, redirect, url_for, flash, session
from app import app, db

@app.route('/', methods=['GET', 'POST'])
def home():
    session.pop('user_id', None)
    session.pop('role', None)
    if 'user_id' not in session:
        return redirect(url_for('login'))
    elif session['role'] == 'student':
        return redirect(url_for('student_dashboard'))
    elif session['role'] == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    else:
        return redirect(url_for('login'))