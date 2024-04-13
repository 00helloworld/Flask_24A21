from flask import render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import FormativeAssessment, UserAttempt

# @app.route('/sdashboard')
# def student_dashboard():
#     """学生仪表板功能"""
#     if 'user_id' not in session or session['role'] != 'student':
#         return redirect(url_for('login'))

#     assessments = FormativeAssessment.query.all()
#     return render_template('student_dashboard.html', assessments=assessments)


@app.route('/attempt_assessment/<int:assessment_id>', methods=['GET', 'POST'])
def attempt_assessment(assessment_id):
    """学生尝试形成性评估功能"""
    if 'user_id' not in session or session['role_id'] != 2:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # 处理学生提交的评估答案并保存
        pass

    assessment = FormativeAssessment.query.get_or_404(assessment_id)
    return render_template('attempt_assessment.html', assessment=assessment)
