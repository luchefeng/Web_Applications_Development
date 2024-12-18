'''
时间：18/12/2024

版本：version 3.0

说明：
本版本实现了：
1.可以在数据库处对食材信息进行数据插入
2.优化了仪表盘界面、登录界面、注册界面，本次新加了一些html文件，
并且原本的HTML文件也有所修改，使得观感更符合人的自然审美
3.本次主要想增加食材管理模块，按照AI提示，新建了models、routes和utils的包，
这样使得原本的用户管理模块和新加的食材管理模块有些混乱
4.这次解决了一些小的报错，主要是网页重定向时出现的RuntimeError（因为当时创建了两个SQLAlchemy 实例，实际上只能创建一个）
AttributeError（应把Session.get()改为session.get()，前者是类，不是方法，后者才是这个类里面的一个方法），
BuilderError（这个url_for和蓝图所用端点有关，解决办法是需要把html中原本的ingredient.update改为ingredient_bp.update_ingredient的样子，
后者应该是代码中定义的样子，而html中的url_for要与它保持一致才能正确匹配）
InvalidRequestError（这个报错出现了两次，第一次是外键没有连接，也就是User和Ingredients没有联系起来。详见“5”。第二个是User类已经开始用了，但是它要用到的Ingredient模型还没被找到，解决办法是把Ingredient模型从ingredient_model.py中捞出来放到app.py中，
再加上实例化的db只能有一个，所以现在整个ingredient_model.py都被注释掉了，
原本的ingredient_routes中需要从ingredient_model.py中导入Ingredient和db，现在改为从app.py中导入了）
5.尝试将User和Ingredients用user_id联系起来，使得一个用户可以有自己的食材操作空间。
这一步使得原本数据库中的Ingredients表被删除，创建了一个新的Ingredients表，其中新增了user_id这一行信息，
这一步在代码中修改的东西是在User类中新增一个ingredients = db.relationship('Ingredient', backref='owner', lazy=True)
在Ingredient类中新增一个user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

待实现功能：
1.之前版本的待实现功能
2.用户的登出页面不太自然，需要改进
3.用户未登录时可以试看网页功能，这里要解决的问题是网页本身（demo）的渲染（目前是以html形式展示）
以及使得demo网页中应包含用户管理信息，现在二者是分开的，无法同时出现在一个页面中，未达到预期效果
4.目前食材管理模块分为无需登录的demo界面和需要登录才能添加、修改、删除食材的页面，现在遇到的问题是，
后者和用户登陆以后该怎么连接起来，是在仪表盘重新输入新的网址吗？一来，输入什么网址？
直接输入食材管理的路由，它显示连接不上，拒绝访问；二来，这样做也不自然，应当是用户登陆后就可以看到修改删除等界面了，
那这些界面如何和我的路由代码联系起来？还是已经联系起来了只是我自己没想明白？
5.在网页实现用户对食材添加、修改和删除，而不是只能从数据库实现
6.明晰两个模块的代码功能，尽可能使代码逻辑清楚，结构清晰，不冗余
7.多熟悉SQL语句，不能老复制粘贴啊

'''

from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import pymysql
from routes.ingredient_routes import ingredient_bp
from flask_session import Session
#from models.ingredient_model import Ingredient
from datetime import datetime

# 加载 .env 文件中的环境变量
load_dotenv()

# 获取环境变量
db_password = os.getenv('DB_PASSWORD')



# 初始化 Flask 应用
app = Flask(__name__)

# 注册蓝图（食材管理模块）
app.register_blueprint(ingredient_bp, url_prefix='/ingredients')

# 配置 MySQL 数据库，正确使用环境变量
app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{db_password}@localhost/flaskdb' # 配置MySQL数据库
#app.config['SECRET_KEY'] = 'your_secret_key'  # 用于加密会话
##app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SESSION_TYPE'] = 'filesystem'  # 使用服务器端会话
#app.config['SQLALCHEMY_ECHO'] = True  # 启用 SQLAlchemy 日志,看看它是否真的在插入新记录

# 初始化扩展
db = SQLAlchemy(app)
Session(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # 未登录时，重定向到 login 视图


class Ingredient(db.Model):
    """
    数据库模型：食材信息
    """
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 唯一标识
    name = db.Column(db.String(100), nullable=False)  # 食材名称
    quantity = db.Column(db.Float, nullable=False, default=0)  # 数量
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键关联到 User 表
    unit = db.Column(db.String(50), nullable=False, default='')  # 单位
    calories = db.Column(db.Float, nullable=True)  # 卡路里
    expiry_date = db.Column(db.DateTime, nullable=True)  # 保质期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间

    def to_dict(self):
        """
        将食材信息转换为字典格式，便于返回 JSON 数据
        """
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'unit': self.unit,
            'calories': self.calories,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }


# 用户模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    calorie_goal = db.Column(db.Integer, default=2000)  # 每日卡路里需求
    ingredients = db.relationship('Ingredient', backref='owner', lazy=True)#使用 db.relationship 来简化查询用户与食材的关系。


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



# 用户加载函数
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


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
            print("用户名或邮箱已存在：", existing_user.username, existing_user.email)  # 添加日志
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
@login_required# 确保用户已登录
def dashboard():
    #user_id = session.get('user_id')  # 获取当前登录用户的 ID（如果你使用 Flask-Login，这个会是 current_user.id）
    user_id = current_user.id  # 直接获取当前登录用户的 ID
    ingredients = Ingredient.query.filter_by(user_id=user_id).all()  # 查询该用户的食材数据
    return render_template('dashboard.html', ingredients=ingredients)
    #return render_template('dashboard.html')  # 用户的主页，示例可以显示食材、卡路里等信息


if __name__ == '__main__':
    with app.app_context():  # 确保在应用上下文中运行
        db.create_all()  # 创建所有模型对应的数据库表
        print("数据库表已创建！")
    app.run(debug=True)
