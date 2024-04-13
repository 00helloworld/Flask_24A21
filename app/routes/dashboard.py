from flask import render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import FormativeAssessment, UserAttempt
from app.models import Question, FormativeAssessment


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

    assessments = FormativeAssessment.query.all()
    return render_template('student_dashboard.html', assessments=assessments)

@app.route('/tdashboard')
def teacher_dashboard():
    """教师仪表板功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    assessments = FormativeAssessment.query.all()
    return render_template('teacher_dashboard.html', assessments=assessments)