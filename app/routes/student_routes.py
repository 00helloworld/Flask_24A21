from flask import render_template, request, redirect, url_for, flash, session
import datetime
from app import app, db
from app.models import User, FormativeAssessment, UserAttempt, AssessmentAttempt, UserAnswer, Question



@app.route('/attempt_assessment/<int:assessment_id>', methods=['GET', 'POST'])
def attempt_assessment(assessment_id):
    """学生尝试形成性评估功能"""
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    assessment = FormativeAssessment.query.get_or_404(assessment_id)
    
    # 判断提交次数
    user_attempts = UserAttempt.query.filter_by(user_id=user.id, assessment_id=assessment.id).count()
    max_attempts = assessment.parameters.get('attempts', 1)  # Default is 1 attempt
    print(max_attempts)
    if user_attempts >= int(max_attempts):
        flash('You have reached the maximum number of attempts for this assessment.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('attempt_assessment.html', assessment=assessment)


@app.route('/submit_attempt/<int:assessment_id>', methods=['POST'])
def submit_attempt(assessment_id):
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    assessment = FormativeAssessment.query.get_or_404(assessment_id)

    # Create a new UserAttempt
    user_attempt = UserAttempt(user_id=user.id, assessment_id=assessment.id, score=0.0)
    db.session.add(user_attempt)
    db.session.commit()

    total_score = 0.0
    correct_answers = 0

    for question in assessment.questions:
        selected_option = request.form.get(f"answer_{question.id}")
        is_correct = selected_option == question.correct_option

        # Update total_score and correct_answers
        if is_correct:
            total_score += 1.0
            correct_answers += 1

        # Create a new UserAnswer
        user_answer = UserAnswer(
            user_attempt_id=user_attempt.id,
            question_id=question.id,
            selected_option=selected_option,
            is_correct=is_correct
        )
        db.session.add(user_answer)

    # Update the UserAttempt with the total_score and answers
    print(type(user_attempt.answers))
    print('******', user_attempt.answers[0].selected_option)
    user_attempt.score = (total_score / len(assessment.questions)) * 100

    db.session.commit()

    flash('Assessment submitted successfully!', 'success')
    return redirect(url_for('dashboard'))  # Change to your dashboard route

