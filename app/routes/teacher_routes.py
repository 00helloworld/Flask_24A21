from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import User, Question, Assessment, AssessmentQuestion


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    """添加问题功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    if request.method == 'POST':
        question_type = request.form.get('question_type')  # 'Type 1'
        if question_type == 'Type1':
            question_text = request.form.get('question_text')
            option_a = request.form.get('option_a')
            option_b = request.form.get('option_b')
            option_c = request.form.get('option_c')
            option_d = request.form.get('option_d')
            correct_option = request.form.get('correct_option')
            correct_answer = 'Type1'
            feedback = request.form.get('feedback')
        else:
            question_text = request.form.get('question_text')
            option_a = 'Type2'
            option_b = 'Type2'
            option_c = 'Type2'
            option_d = 'Type2'
            correct_option = 'Type2'
            correct_answer = request.form.get('correct_answer')
            feedback = request.form.get('feedback')
        

        question = Question(question_text=question_text, option_a=option_a, option_b=option_b,
                            option_c=option_c, option_d=option_d, correct_option=correct_option,
                            correct_answer=correct_answer, feedback=feedback, question_type=question_type)
        
        db.session.add(question)
        db.session.commit()

        flash('Question added successfully', 'success')
        return redirect(url_for('manage_questions'))

    return render_template('add_question.html')


@app.route('/manage_questions', methods=['GET'])
def manage_questions():
    """查看所有问题功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    question_type = request.args.get('type')  # 获取查询参数，默认为'all'

    if question_type == 'type1':
        questions = Question.query.filter_by(question_type='Type1').all()
    elif question_type == 'type2':
        questions = Question.query.filter_by(question_type='Type2').all()
    else:
        questions = Question.query.all()

    return render_template('manage_questions.html', questions=questions, selected_type=question_type)

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
        return redirect(url_for('manage_questions'))

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
    return redirect(url_for('manage_questions'))




@app.route('/add_assessment', methods=['GET', 'POST'])
def add_assessment():
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('assessment_type')
        duration = request.form.get('duration')
        deadline = request.form.get('deadline')
        attempts = request.form.get('attempts')
        feedback = True if request.form.get('feedback') else False
        selected_questions = request.form.getlist('selected_questions[]')
        # selected_questions = [int(id) for id in request.form.getlist('selected_questions[]') if id.isdigit()]
        print(len(selected_questions))

        # Create a new assessment
        new_assessment = Assessment(name=name, type=type, parameters={
            'duration': duration,
            'deadline': deadline,
            'attempts': attempts,
            'feedback': feedback
        })
        db.session.add(new_assessment)

        # Add selected questions to the assessment
        for question_id in selected_questions:
            print('*'*50, question_id)
            question = Question.query.get(question_id)
            if question:
                assessment_question = AssessmentQuestion(assessment_id=new_assessment.id, question_id=question.id)
                db.session.add(assessment_question)

        try:
            
            db.session.commit()
            flash('Assessment added successfully!', 'success')
            return redirect(url_for('manage_assessments'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            print('*'*50, 'ERROR')

    questions = Question.query.all()
    return render_template('add_assessment.html', questions=questions)



@app.route('/edit_assessment/<int:assessment_id>', methods=['GET', 'POST'])
def edit_assessment(assessment_id):
    # Get the assessment to edit
    assessment = Assessment.query.get_or_404(assessment_id)

    if request.method == 'POST':
        name = request.form.get('name')
        duration = request.form.get('duration')
        deadline = request.form.get('deadline')
        attempts = request.form.get('attempts')
        feedback = True if request.form.get('feedback') else False
        selected_questions = request.form.getlist('selected_questions[]')
        print(len(selected_questions))

        if True:# try:
            # Update the assessment
            assessment.name = name
            assessment.parameters = {
                'duration': duration,
                'deadline': deadline,
                'attempts': attempts,
                'feedback': feedback
            }

            # Clear existing questions from the assessment
            assessment.questions.clear()
            AssessmentQuestion.query.filter_by(assessment_id=assessment.id).delete()
            
            

            # Add selected questions to the assessment
            for question_id in selected_questions:
                print('*'*50, question_id)
                question = Question.query.get(question_id)
                if question:
                    assessment_question = AssessmentQuestion(assessment_id=assessment.id, question_id=question.id)
                    db.session.add(assessment_question)

            db.session.commit()
            flash('Assessment updated successfully!', 'success')
            return redirect(url_for('manage_assessments'))

        else: # except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
            print('*'*50, 'EDIT ERROR')

    questions = Question.query.all()
    return render_template('edit_assessment.html', assessment=assessment, questions=questions)

@app.route('/delete_assessment/<int:assessment_id>', methods=['POST'])
def delete_assessment(assessment_id):
    """删除形成性评估功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    assessment = Assessment.query.get(assessment_id)
    if assessment:
        db.session.delete(assessment)
        db.session.commit()
        flash('Assessment deleted successfully', 'success')
    else:
        flash('Assessment not found', 'error')

    return redirect(url_for('manage_assessments'))

@app.route('/manage_assessments', methods=['GET'])
def manage_assessments():
    """管理评估功能"""
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))

    f_assessments = Assessment.query.filter_by(type='FORMATIVE').all()
    s_assessments = Assessment.query.filter_by(type='SUMMATIVE').all()

    return render_template('manage_assessments.html', f_assessments=f_assessments, s_assessments=s_assessments)