from flask import Blueprint, request, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from models2 import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from captcha.image import ImageCaptcha
import random, string

users_bp = Blueprint('users', __name__)

# 用户列表
@users_bp.route('/')
def index():
    users = User.query.all()
    users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify({'message': '用户列表获取成功', 'data': users_data}), 200

# 单个用户信息
@users_bp.route('/<int:id>')
def user(id):
    user = User.query.get(id)
    if user:
        return jsonify({'message': '用户信息获取成功', 'data': {'id': user.id, 'username': user.username, 'email': user.email}}), 200
    else:
        return jsonify({'message': '用户不存在'}), 404

# 用户注册
@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not email or not password or not username:
        return jsonify({'message': '用户名、邮箱和密码不能为空'}), 400

    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'message': '用户名或邮箱已存在，请选择其他的'}), 400

    try:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': '注册成功！请登录。'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'注册失败: {str(e)}'}), 500

# 用户登录
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    captcha = data.get('captcha')

    if 'captcha' not in session or session['captcha'] != captcha:
        return jsonify({'message': '验证码错误！'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': '用户名不存在，请先注册。'}), 400

    if user and user.check_password(password):
        login_user(user)
        session['user_id'] = user.id
        return jsonify({'message': '登录成功！', 'data': {'user_id': user.id, 'username': user.username}}), 200
    else:
        return jsonify({'message': '密码错误，请重试。'}), 400

# 用户登出
@users_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    return jsonify({'message': '您已登出。'}), 200

# 用户仪表盘
@users_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user
    return jsonify({'message': '仪表盘数据获取成功', 'data': {'username': user.username, 'email': user.email}}), 200

# 用户信息
@users_bp.route('/user-info')
@login_required
def user_info():
    user = current_user
    return jsonify({'message': '用户信息获取成功', 'data': {'username': user.username, 'email': user.email}}), 200

# 删除账户
@users_bp.route('/delete_account/<int:id>', methods=['POST'])
@login_required
def delete_account(id):
    user_to_delete = User.query.get(id)
    if user_to_delete and user_to_delete.id == current_user.id:
        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({'message': '用户已成功注销'}), 200
    else:
        return jsonify({'message': '未找到该用户或没有权限'}), 403

# 生成验证码
@users_bp.route('/generate-captcha', methods=['GET'])
def generate_captcha():
    image = ImageCaptcha()
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    session['captcha'] = captcha_text
    captcha_image = image.generate(captcha_text)
    response = jsonify({'message': '验证码生成成功', 'data': {'captcha': captcha_text}})
    return response, 200

# 验证验证码
@users_bp.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    user_input = request.json.get('captcha')
    captcha_in_session = session.get('captcha')
    if captcha_in_session and captcha_in_session == user_input:
        return jsonify({'message': '验证码正确！'}), 200
    else:
        return jsonify({'message': '验证码错误！'}), 400