from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, login_required, logout_user, current_user
from models2 import db, User, UserProfile
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/')
def index():
    users = User.query.all()
    return render_template('users/operations.html', users=users)

@users_bp.route('/<int:id>')
def user(id):
    user = User.query.get(id)
    return render_template('users/profile.html', user=user)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        if not email:
            flash('电子邮件不能为空')
            return redirect(url_for('users.register'))

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('用户名或邮箱已存在，请选择其他的')
            return redirect(url_for('users.register'))

        try:
            new_user = User(username=username, email=email, password_hash=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('注册成功！请登录。')
        except:
            db.session.rollback()
            flash('注册失败，请重试。')

        return redirect(url_for('users.index'))
    return render_template('users/operations.html')

@users_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        flash('用戶名不存在，請先註冊。')
        return redirect(url_for('users.register'))

    if user and user.check_password(password):
        login_user(user)
        flash('登錄成功！')
        return redirect(url_for('users.dashboard'))
    else:
        flash('密碼錯誤，請重試。')
        return redirect(url_for('users.index'))

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

@users_bp.route('/delete_account/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    user_to_delete = User.query.get(id)
    if user_to_delete and user_to_delete.id == current_user.id:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('用戶已成功注銷', 'success')
    else:
        flash('未找到該用戶或沒有權限', 'error')
    return redirect(url_for('users.index'))


@users_bp.route('/reset_password', methods=['POST'])
def reset_password():
    '''重置密码视图'''
    email = request.form['email']
    user = User.query.filter_by(email=email).first()

    if user:
        # 这里可以发送重置密码的电子邮件，实际情况中需要实现邮件发送功能
        flash('重置密码的链接已发送至您的邮箱。')
    else:
        flash('该电子邮件未注册。')
    return redirect(url_for('users.index'))


@users_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        avatar_url = request.form.get('avatar_url')
        nickname = request.form.get('nickname')
        bio = request.form.get('bio')

        if current_user.profile:
            current_user.profile.avatar_url = avatar_url
            current_user.profile.nickname = nickname
            current_user.profile.bio = bio
        else:
            new_profile = UserProfile(user_id=current_user.id, avatar_url=avatar_url, nickname=nickname, bio=bio)
            db.session.add(new_profile)

        db.session.commit()
        flash('個人資料更新成功！')
        return redirect(url_for('users.dashboard'))

    return render_template('users/profile.html', user=current_user)
