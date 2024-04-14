from flask import render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import UserAttempt
from app.models import Question, Assessment, User


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login!')
        return redirect(url_for('login'))
    elif session['role'] == 'student':
        return redirect(url_for('student_dashboard'))
    elif session['role'] == 'teacher':
        return redirect(url_for('teacher_dashboard'))
    else:
        flash('Error!')
        return redirect(url_for('login'))


@app.route('/sdashboard')
def student_dashboard():
    """学生仪表板功能"""
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    f_assessments = Assessment.query.filter_by(type='FORMATIVE').all()
    s_assessments = Assessment.query.filter_by(type='SUMMATIVE').all()

    user = User.query.get(session['user_id'])
    if user:
        user_attempts = UserAttempt.query.filter_by(user_id=user.id)
    else:
        return redirect(url_for('home'))
    
    return render_template('student_dashboard.html', f_assessments=f_assessments, s_assessments=s_assessments, user_attempts=user_attempts)

@app.route('/tdashboard')
def teacher_dashboard():
    """教师仪表板功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if user:
        pass
    else:
        return redirect(url_for('home'))

    assessments = Assessment.query.all()
    return render_template('teacher_dashboard.html', assessments=assessments)