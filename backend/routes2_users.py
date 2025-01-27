'''
2025.1.26
用戶功能规划：
1.基本內容注册、登录（含验证码）、忘记密码、修改密码、修改个人信息、查看个人信息、查看其他用户信息、注销账户、
驗證密碼（若錯誤則拒絕登入）、驗證郵箱（若未註冊則拒絕發送重置郵件）、驗證用戶名（若已存在則拒絕註冊）、

2.進階內容：用戶頭像、用戶背景、用戶簽名、用戶等級、用戶積分、用戶勳章、用戶等級、用戶設置、用戶隱私、用戶安全

3.用戶體驗提升
        用戶資料管理: 用戶可以查看和更新個人信息（如姓名、郵箱、電話等）。
        多因素驗證（MFA）: 增加額外的安全層，除了密碼外，還需要其他形式的驗證（例如，短信或電子郵件的驗證碼）。
        用戶偏好設定: 允許用戶設置個性化的偏好，例如界面主題、語言等。
        活動日誌: 提供用戶活動記錄，可以查看最近的登錄時間、IP地址等，增加透明度和安全感。
        通知與消息: 用戶可以收到系統通知和消息，例如新功能上線、系統維護提醒等。
        帳戶安全檢查: 定期提醒用戶檢查和更新安全設置，如密碼強度、未使用的帳號等。
        社交登入: 支持用戶使用社交媒體賬號（如Google、Facebook）快速註冊和登錄。
        用戶反饋: 提供反饋渠道，讓用戶可以報告問題或提出建議。
'''
from models2 import db
from flask  import Blueprint, render_template, request, redirect, url_for, flash
from models2 import User
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__) # 创建用戶蓝图

@users_bp.route('/') # 設置用戶视图路由
def index():
    '''用戶视图'''
    users = User.query.all() # 查询所有用戶
    return render_template('users/operations.html', users=users)

@users_bp.route('/<int:id>') # 設置用戶详情视图路由
def user(id):
    '''用戶详情视图'''
    user = User.query.get(id) # 查询用戶
    return render_template('users/user.html', user=user)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    '''注册视图'''
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        print(f"Received data: username={username}, email={email}, password={password}")

        if not email:
            flash('电子邮件不能为空')
            return redirect(url_for('users.register'))

        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('用户名已存在，请选择其他用户名')
            return redirect(url_for('users.register'))

        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('注册成功！请登录。')
        return redirect(url_for('users.index'))
    return render_template('users/operations.html')  # 渲染 operations.html


@users_bp.route('/login', methods=['POST'])
def login():
    '''登录视图'''
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        flash('登录成功！')
        return redirect(url_for('users.index'))
    else:
        flash('用户名或密码错误，请重试。')
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