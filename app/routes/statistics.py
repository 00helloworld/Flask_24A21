from flask import render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import UserAttempt
from app.models import Question, Assessment, User


@app.route('/teacher_statistics', methods=['GET', 'POST'])
def teacher_statistics():
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    
    # test
    users = db.session.query(User).all()
    print("*"*10, users[1].attempts)
    #
    
    query = db.session.query(UserAttempt).join(User, UserAttempt.user_id==User.id)

    if request.method == 'POST':
        # Filter and sort data based on selected criteria
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        assessment_type = request.form.get('assessment_type')
        
        if date_from and date_to:
            query = query.filter(
                UserAttempt.timestamp.between(date_from, date_to)
            )
        
        if assessment_type:
            query = query.join(Assessment).filter(
                Assessment.name == assessment_type
            )

    attempts = query.all()
    assessments = Assessment.query.all()
    

    return render_template('teacher_statistics.html', attempts=attempts, assessments=assessments)