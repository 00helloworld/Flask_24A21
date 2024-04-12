from flask import render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import Question, FormativeAssessment

@app.route('/tdashboard')
def teacher_dashboard():
    """教师仪表板功能"""
    if 'user_id' not in session or session['role_id'] != 1:
        return redirect(url_for('routes.login'))

    assessments = FormativeAssessment.query.all()
    return render_template('teacher_dashboard.html', assessments=assessments)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    """添加问题功能"""
    if 'user_id' not in session or session['role_id'] != 1:
        return redirect(url_for('routes.login'))

    if request.method == 'POST':
        question_text = request.form.get('question_text')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_option = request.form.get('correct_option')
        feedback = request.form.get('feedback')
        question_type = 'Type I'

        question = Question(question_text=question_text, option_a=option_a, option_b=option_b,
                            option_c=option_c, option_d=option_d, correct_option=correct_option,
                            feedback=feedback, question_type=question_type)
        
        db.session.add(question)
        db.session.commit()

        flash('Question added successfully', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('add_question.html')

@app.route('/add_assessment', methods=['GET', 'POST'])
def add_assessment():
    """添加形成性评估功能"""
    if 'user_id' not in session or session['role_id'] != 1:
        return redirect(url_for('routes.login'))

    if request.method == 'POST':
        assessment_name = request.form.get('assessment_name')
        duration = request.form.get('duration')
        end_date = request.form.get('end_date')
        attempts_allowed = request.form.get('attempts_allowed')
        immediate_feedback = request.form.get('immediate_feedback') == 'on'

        assessment = FormativeAssessment(assessment_name=assessment_name, duration=duration,
                                         end_date=end_date, attempts_allowed=attempts_allowed,
                                         immediate_feedback=immediate_feedback)
        
        db.session.add(assessment)
        db.session.commit()

        flash('Assessment added successfully', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('add_assessment.html')
