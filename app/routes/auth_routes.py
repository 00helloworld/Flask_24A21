from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash

from app import app, db
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录功能"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            else:
                return redirect(url_for('student_dashboard'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """用户注销功能"""
    session.pop('user_id', None)
    session.pop('role', None)
    flash('Successfully logout!')
    return redirect(url_for('login'))


@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    """学生注册功能"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register_student'))

        new_user = User(username=username, role='student')
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('register_student.html')

@app.route('/register/teacher', methods=['GET', 'POST'])
def register_teacher():
    """老师注册功能"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register_teacher'))

        new_user = User(username=username, role='teacher')
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('You have successfully registered!', 'success')
        return redirect(url_for('login'))

    return render_template('register_teacher.html')
