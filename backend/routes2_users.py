from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from models2 import db, User
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def index():
    users = User.query.all()
    return render_template('users/operations.html', users=users)

@users_bp.route('/<int:id>')
def user(id):
    user = User.query.get(id)
    return render_template('users/user.html', user=user)

@users_bp.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if not email:
            return {'message': '電子郵件不能為空'}, 400

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return {'message': '用戶名或郵箱已存在，請選擇其他的'}, 400

        try:
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return {'message': '註冊成功！請登錄。'}, 201
        except:
            db.session.rollback()
            return {'message': '註冊失敗，請重試。'}, 500

@users_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return {'message': '用戶名不存在，請先註冊。'}, 400

    if user and user.check_password(password):
        session['user_id'] = user.id  # 使用 session 儲存用戶 ID
        return {'message': '登錄成功！'}, 200
    else:
        return {'message': '密碼錯誤，請重試。'}, 400

@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('_flashes', None)  # 清除之前的 flash 消息
    logout_user()
    flash('您已登出。')
    return redirect(url_for('users.index'))

@users_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('users/dashboard.html', user=current_user)

@users_bp.route('/user-info')
@login_required
def user_info():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return {
        'username': user.username,
        'email': user.email
    }

@users_bp.route('/delete_account/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    user_to_delete = User.query.get(id)
    if user_to_delete and user_to_delete.id == current_user.id:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('用戶已成功註銷', 'success')
    else:
        flash('未找到該用戶或沒有權限', 'error')
    return redirect(url_for('users.index'))

@users_bp.route('/reset_password', methods=['POST'])
def reset_password():
    '''重置密碼視圖'''
    email = request.form['email']
    user = User.query.filter_by(email=email).first()

    if user:
        # 這裡可以發送重置密碼的電子郵件，實際情況中需要實現郵件發送功能
        flash('重置密碼的鏈接已發送至您的郵箱。')
    else:
        flash('該電子郵件未註冊。')
    return redirect(url_for('users.index'))
