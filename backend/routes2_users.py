from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask_login import login_user, login_required, logout_user, current_user
from models2 import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from captcha.image import ImageCaptcha
import random, string

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
        calorie_version = request.json.get('calorieVersion', False)  # 获取是否选择卡路里管理版本
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        print(f"Received calorie_version: {calorie_version}")  # 添加日志

        if not email:
            return {'message': '电子邮件不能为空'}, 400

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            return {'message': '用户名或邮箱已存在，请选择其他的'}, 400

        try:
            new_user = User(username=username, email=email, password_hash=hashed_password,
                            calorie_version=calorie_version)
            db.session.add(new_user)
            db.session.commit()

            # 新增用戶後立即檢查用戶是否在數據庫中
            user = User.query.filter_by(username='ten').first()
            print(f"User in database: {user}")
            print(f"User registered with calorie version: {calorie_version}")  # 添加日志

            return {'message': '注册成功！请登录。', 'calorie_version': calorie_version}, 201
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {e}")
            return {'message': '注册失败，请重试。'}, 500

@users_bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    captcha = request.json.get('captcha')

    print(f"Session ID: {session.sid}, CAPTCHA in session: {session.get('captcha')}")  # 添加日志

    if 'captcha' not in session or session['captcha'] != captcha:
        print("验证码错误，登录失败")
        return {'message': '验证码错误！'}, 400

    user = User.query.filter_by(username=username).first()
    print(f"Querying user: {username}, Found: {user}")

    if not user:
        print("用户名不存在，登录失败")
        return {'message': '用户名不存在，请先注册。'}, 400

    if user and user.check_password(password):
        session['user_id'] = user.id  # 使用 session 保存用户 ID
        login_user(user)  # 登录用户
        print(f"User {user.username} logged in successfully.")  # 增加登录成功日志
        response_data = {
            'message': '登录成功！',
            'user_id': user.id,  # 添加 user_id 字段
            'calorie_version': user.calorie_version,  # 返回用户版本信息
            'username': user.username,
            'email': user.email
        }
        print(f"返回的响应数据: {response_data}")
        return jsonify(response_data), 200
    else:
        print("密码错误，登录失败")
        return {'message': '密码错误，请重试。'}, 400

@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    print('Logout request received.')  # 添加日誌
    session.pop('_flashes', None)  # 清除之前的 flash 消息
    logout_user()
    print('User logged out.')  # 添加日誌
    return jsonify({'message': '您已成功登出。'}), 200

@users_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return jsonify({'message': '歡迎來到儀表板！', 'user': {'username': current_user.username, 'email': current_user.email}}), 200

@users_bp.route('/user-info', methods=['GET'])
@login_required
def user_info():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    return {
        'username': user.username,
        'email': user.email
    }, 200

@users_bp.route('/delete_account/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    user_to_delete = User.query.get(id)
    if user_to_delete and user_to_delete.id == current_user.id:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({'message': '用戶已成功註銷'}), 200
    else:
        return jsonify({'message': '未找到該用戶或沒有權限'}), 404

@users_bp.route('/reset_password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        # 假設這裡有一個發送郵件的邏輯
        return jsonify({'message': '重置密碼的鏈接已發送至您的郵箱。'}), 200
    else:
        return jsonify({'message': '該電子郵件未註冊。'}), 404

@users_bp.route('/generate-captcha', methods=['GET'])
def generate_captcha():
    image = ImageCaptcha()
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    session['captcha'] = captcha_text
    print(f"Session ID: {session.sid}, CAPTCHA: {captcha_text}")  # 添加日誌
    captcha_image = image.generate(captcha_text)
    response = make_response(captcha_image.read())
    response.headers['Content-Type'] = 'image/png'
    return response

@users_bp.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    user_input = request.json.get('captcha')
    captcha_in_session = session.get('captcha')
    print(f"Received CAPTCHA: {user_input}, Session CAPTCHA: {captcha_in_session}")  # 添加日誌
    if captcha_in_session and captcha_in_session == user_input:
        return jsonify({'message': '驗證碼正確！'}), 200
    else:
        return jsonify({'message': '驗證碼錯誤！'}), 400