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
            session['role_id'] = user.role_id
            return redirect(url_for('routes.dashboard'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    """用户注销功能"""
    session.pop('user_id', None)
    session.pop('role_id', None)
    return redirect(url_for('routes.login'))
