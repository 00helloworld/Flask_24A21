from flask import render_template, request, redirect, url_for, flash, session

from app import app, db
from app.models import UserAttempt
from app.models import Question, Assessment, User
from sqlalchemy import func, cast, DateTime
from datetime import datetime


@app.route('/teacher_statistics', methods=['GET', 'POST'])
def teacher_statistic():
    if 'user_id' not in session or session['role'] != 'teacher':
        return redirect(url_for('login'))
    
    # 获取session['user_id']对应的UserAttempt数据
    user_attempts = UserAttempt.query.filter_by().all()

    assessments_id_filter = None
    if request.method == 'POST':
        type_ = request.form.get('assessment_type')
        start_time = request.form.get('start_time')  # Not filled will be ''
        end_time = request.form.get('end_time')

        assessments_id_filter = ass_filter(type_, start_time, end_time)
        
        print('-'*10, assessments_id_filter)
    
    formatted_assessments, all_students = attempt_format(user_attempts, assessments_id_filter)


    print('*'*10)
    print(formatted_assessments)
    print('*'*10)
    return render_template('statistics_teacher.html', assessments=formatted_assessments, all_students=all_students)



@app.route('/student_statistics/<student_id>', methods=['GET', 'POST'])
def student_statistic(student_id=None):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # 获取session['user_id']对应的UserAttempt数据
    if session['role'] == 'student':
        user_attempts = UserAttempt.query.filter_by(user_id=session['user_id']).all()
    elif student_id:
        user_attempts = UserAttempt.query.filter_by(user_id=student_id).all()
    else:
        return redirect(url_for('login'))
    
    assessments_id_filter = None
    if request.method == 'POST':
        type_ = request.form.get('assessment_type')
        start_time = request.form.get('start_time')  # Not filled will be ''
        end_time = request.form.get('end_time')

        assessments_id_filter = ass_filter(type_, start_time, end_time)
        
        print('-'*10, assessments_id_filter)
        # print('-'*10, datetime.strptime(start_time, '%Y-%m-%dT%H:%M'))
    
    student_name = user_attempts[0].user_name
    
    formatted_assessments, all_students = attempt_format(user_attempts, assessments_id_filter)

    all_assessments = Assessment.query.all()
    student_complete_rate = round(len(formatted_assessments) / len(all_assessments) * 100, 1)

    print('*'*10)
    print(formatted_assessments)
    print('*'*10)
    return render_template('statistics_student.html', 
                           assessments=formatted_assessments, 
                           student_complete_rate=student_complete_rate, 
                           role=session['role'], 
                           student_name=student_name)


def ass_filter(type_, start_time, end_time):
    print(type_)
    print(start_time)
    print(end_time)
    assessments_ = Assessment.query

    if type_ == 'All':
        pass
    else:
        assessments_ = assessments_.filter_by(type=type_)

    assessments_list = assessments_.all()
    assessments_id_filter = []
    if start_time != '' and end_time != '':
        for ass in assessments_list:
            if datetime.strptime(ass.parameters['deadline'], '%Y-%m-%dT%H:%M') >= datetime.strptime(start_time, '%Y-%m-%dT%H:%M') \
                and datetime.strptime(ass.parameters['deadline'], '%Y-%m-%dT%H:%M') <= datetime.strptime(end_time, '%Y-%m-%dT%H:%M'):
                assessments_id_filter.append(ass.id)
        
    elif start_time != '' and end_time == '':
        for ass in assessments_list:
            if datetime.strptime(ass.parameters['deadline'], '%Y-%m-%dT%H:%M') >= datetime.strptime(start_time, '%Y-%m-%dT%H:%M'):
                assessments_id_filter.append(ass.id)
        
    elif start_time == '' and end_time != '':
        for ass in assessments_list:
            if datetime.strptime(ass.parameters['deadline'], '%Y-%m-%dT%H:%M') <= datetime.strptime(end_time, '%Y-%m-%dT%H:%M'):
                assessments_id_filter.append(ass.id)
    else:
        for ass in assessments_list:
            assessments_id_filter.append(ass.id)

    return assessments_id_filter


def attempt_format(user_attempts, assessments_id_filter):
    assessments = {}

    print('-'*10, assessments_id_filter)
    for attempt in user_attempts:
        if assessments_id_filter is None:
            if attempt.assessment_name not in assessments:
                assessments[attempt.assessment_name] = {
                    'count': 0,
                    'max_score': None,
                    'min_score': None,
                    'avg_score': 0,
                    'scores': [],
                    'students': []
                }
            
            # 更新统计数据
            assessments[attempt.assessment_name]['count'] += 1
            assessments[attempt.assessment_name]['scores'].append(attempt.score)
            assessments[attempt.assessment_name]['students'].append(attempt.user_name)
            
            if assessments[attempt.assessment_name]['max_score'] is None or attempt.score > assessments[attempt.assessment_name]['max_score']:
                assessments[attempt.assessment_name]['max_score'] = attempt.score
            
            if assessments[attempt.assessment_name]['min_score'] is None or attempt.score < assessments[attempt.assessment_name]['min_score']:
                assessments[attempt.assessment_name]['min_score'] = attempt.score
        elif attempt.assessment_id in assessments_id_filter:
            if attempt.assessment_name not in assessments:
                assessments[attempt.assessment_name] = {
                    'count': 0,
                    'max_score': None,
                    'min_score': None,
                    'avg_score': 0,
                    'scores': [],
                    'students': []
                }
            
            # 更新统计数据
            assessments[attempt.assessment_name]['count'] += 1
            assessments[attempt.assessment_name]['scores'].append(attempt.score)
            assessments[attempt.assessment_name]['students'].append(attempt.user_name)
            
            if assessments[attempt.assessment_name]['max_score'] is None or attempt.score > assessments[attempt.assessment_name]['max_score']:
                assessments[attempt.assessment_name]['max_score'] = attempt.score
            
            if assessments[attempt.assessment_name]['min_score'] is None or attempt.score < assessments[attempt.assessment_name]['min_score']:
                assessments[attempt.assessment_name]['min_score'] = attempt.score


    # 计算avg_score
    for assessment in assessments.values():
        assessment['avg_score'] = sum(assessment['scores']) / assessment['count'] if assessment['count'] > 0 else 0
        assessment['student_cnt'] = len(set(assessment['students']))
    all_students = User.query.filter(User.role=='student').all()

    # 将数据格式化为所需的结构
    formatted_assessments = [{
        'ass_name': f"{assessment_name}",
        'atempt_times': assessment['count'],
        'avg_score': assessment['avg_score'],
        'min_score': assessment['min_score'],
        'max_score': assessment['max_score'],
        'scores': assessment['scores'],
        'student_cnt': assessment['student_cnt'],
        'all_student_cnt': len(all_students),
        'ass_complete_rate': round(assessment['student_cnt']/len(all_students)*100, 1)
    } for assessment_name, assessment in assessments.items()]

    return formatted_assessments, all_students