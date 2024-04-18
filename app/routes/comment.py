from flask import render_template, request, jsonify, redirect, url_for, flash, session
from app import app, db
from app.models import Comment, User
import os
from datetime import datetime


@app.route('/comments', methods=['get'])
def comments():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).one()
    comments = Comment.query.all()
    print('-'*10, comments)
    print('-'*10, user)

    return render_template('comments.html', comments=comments, user=user)

@app.route('/comments_logs', methods=['get'])
def comment_log():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    comments = Comment.query.all()
    return render_template('comments_logs.html', comments=comments)


@app.route('/post_comment', methods=['POST'])
def post_comment():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).one()
    
    content = request.form.get('content')
    image_path = None
    if 'image' in request.files and request.files['image'].filename != '':
        image_path = save_image(request.files['image'])
    
    parent_id = request.form.get('parent_id', None)

    comment = Comment(user_id=user_id, user_name=user.username, 
                      user_role=user.role, content=content,
                      image=image_path, parent_id=parent_id)
    db.session.add(comment)
    db.session.commit()
    print('-'*30, session['user_id'])
    flash('Your comment has been posted!', 'success')
    return redirect(url_for('comments'))

@app.route('/delete_comment/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    
    comment = Comment.query.get_or_404(comment_id)
    if user_id != comment.user_id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/delete_reply/<int:reply_id>', methods=['DELETE'])
def delete_reply(reply_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    
    reply = Comment.query.get_or_404(reply_id)
    if user_id != reply.user_id:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    db.session.delete(reply)
    db.session.commit()
    return jsonify({'success': True})

def save_image(image):
    # 保存图片并返回路径
    image_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.jpg"
    image_path = os.path.join('app/static/images', image_name)
    image.save(image_path)
    return image_name
