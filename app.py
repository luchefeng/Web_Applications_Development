from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import pymysql

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取环境变量
db_password = os.getenv('DB_PASSWORD')


""""# 初始化Flask应用
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:db_password@localhost/flaskdb'  # 配置MySQL数据库
app.config['SECRET_KEY'] = 'your_secret_key'  # 用于加密会话
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 未登录时，重定向到login视图
"""
# 初始化 Flask 应用
app = Flask(__name__)

# 配置 MySQL 数据库，正确使用环境变量
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{db_password}@localhost/flaskdb' # 配置MySQL数据库
app.config['SECRET_KEY'] = 'your_secret_key'  # 用于加密会话
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 未登录时，重定向到 login 视图


# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    calorie_goal = db.Column(db.Integer, default=2000)  # 每日卡路里需求

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 用户注册视图
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 检查用户名或邮箱是否已存在
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("用户名或邮箱已存在", "danger")
            return redirect(url_for('register'))

        # 创建新用户
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("注册成功！请登录", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# 用户登录视图
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 查找用户并验证密码
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash("登录成功！", "success")
            return redirect(url_for('dashboard'))  # 登录后跳转到用户主页

        flash("用户名或密码错误", "danger")

    return render_template('login.html')


# 用户注销视图
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("您已注销", "info")
    return redirect(url_for('login'))


# 用户主页（需要登录）
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')  # 用户的主页，示例可以显示食材、卡路里等信息


if __name__ == '__main__':
    with app.app_context():  # 确保在应用上下文中运行
        db.create_all()  # 创建所有模型对应的数据库表
        print("数据库表已创建！")
    app.run(debug=True)
