from flask import render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import Question, FormativeAssessment

# @app.route('/tdashboard')
# def teacher_dashboard():
#     """教师仪表板功能"""
#     if 'user_id' not in session or session['role'] != 1:
#         return redirect(url_for('login'))

#     assessments = FormativeAssessment.query.all()
#     return render_template('teacher_dashboard.html', assessments=assessments)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    """添加问题功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    if request.method == 'POST':
        question_text = request.form.get('question_text')
        option_a = request.form.get('option_a')
        option_b = request.form.get('option_b')
        option_c = request.form.get('option_c')
        option_d = request.form.get('option_d')
        correct_option = request.form.get('correct_option')
        feedback = request.form.get('feedback')
        question_type = request.form.get('question_type')  # 'Type 1'

        question = Question(question_text=question_text, option_a=option_a, option_b=option_b,
                            option_c=option_c, option_d=option_d, correct_option=correct_option,
                            feedback=feedback, question_type=question_type)
        
        db.session.add(question)
        db.session.commit()

        flash('Question added successfully', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_question.html')



@app.route('/view_questions', methods=['GET'])
def view_questions():
    """查看所有问题功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    questions = Question.query.all()
    return render_template('view_questions.html', questions=questions)

@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    """编辑问题功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    question = Question.query.get_or_404(question_id)

    if request.method == 'POST':
        question.question_type = request.form.get('question_type')
        question.question_text = request.form.get('question_text')
        question.option_a = request.form.get('option_a')
        question.option_b = request.form.get('option_b')
        question.option_c = request.form.get('option_c')
        question.option_d = request.form.get('option_d')
        question.correct_option = request.form.get('correct_option')
        question.feedback = request.form.get('feedback')

        db.session.commit()

        flash('Question updated successfully', 'success')
        return redirect(url_for('view_questions'))

    return render_template('edit_question.html', question=question)

@app.route('/delete_question/<int:question_id>', methods=['POST'])
def delete_question(question_id):
    """删除问题功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()

    flash('Question deleted successfully', 'success')
    return redirect(url_for('view_questions'))


@app.route('/add_assessment', methods=['GET', 'POST'])
def add_assessment():
    """添加形成性评估功能"""
    if 'user_id' not in session or session['role'] != 1:
        return redirect(url_for('login'))

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
        return redirect(url_for('dashboard'))

    return render_template('add_assessment.html')
