from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()  # 创建SQLAlchemy实例

class User(db.Model, UserMixin):
    '''用户模型'''
    __tablename__ = 'user'  # 确保表名是user，而不是users
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自動增長
    username = db.Column(db.String(255), unique=True, nullable=False)  # 用户名
    email = db.Column(db.String(255), unique=True, nullable=False)  # 邮箱
    password_hash = db.Column(db.String(255), nullable=False)  # 密码哈希
    calorie_goal = db.Column(db.Integer, default=2000)  # 卡路里目标
    profile = db.relationship('UserProfile', uselist=False, back_populates='user')  # 个人资料
    ingredients = db.relationship('Ingredient', backref='user', lazy=True) # 食材管理

    def set_password(self, password):
        '''设置密码'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''检查密码'''
        return check_password_hash(self.password_hash, password)

class UserProfile(db.Model):
    '''用户资料模型'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自動增長
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键
    avatar_url = db.Column(db.String(255))  # 頭像URL
    nickname = db.Column(db.String(255))  # 昵稱
    bio = db.Column(db.Text)  # 個性簽名

    user = db.relationship('User', back_populates='profile')  # 使用 back_populates 而不是 backref

class Recipes(db.Model):
    '''食谱模型'''
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(255), nullable=False)  # 标题
    ingredients = db.Column(db.Text, nullable=False)  # 食材
    instructions = db.Column(db.Text, nullable=False)  # 做法
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))  # 关系

    def __repr__(self):
        '''返回一个可读字符串'''
        return f'<Recipe {self.title}>'

class Article(db.Model):
    '''文章模型'''
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(255), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # 内容
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 外键
    user = db.relationship('User', backref=db.backref('articles', lazy=True))  # 关系

    def __repr__(self):
        '''返回一个可读字符串'''
        return f'<Article {self.title}>'

class CalorieGoal(db.Model):
    __tablename__ = 'calorie_goal'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    __table_args__ = {'extend_existing': True}

class CalorieIntake(db.Model):
    __tablename__ = 'calorie_intake'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    intake = db.Column(db.Integer, nullable=False)
    meal_time = db.Column(db.String(50), nullable=False)
    food_item = db.Column(db.String(150), nullable=False)
    __table_args__ = {'extend_existing': True}

class WeightRecord(db.Model):
    __tablename__ = 'weight_record'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    __table_args__ = {'extend_existing': True}

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    shelf_life = db.Column(db.Integer, nullable=False)  # 保質期（天數）
    quantity = db.Column(db.Float, nullable=False)  # 數量
    unit_calories = db.Column(db.Float, nullable=False)  # 單位卡路里數目
    purchase_date = db.Column(db.Date, nullable=False)  # 購買日期
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 更改這行，指向user表的id

    def __init__(self, name, category, shelf_life, quantity, unit_calories, purchase_date, user_id):
        self.name = name
        self.category = category
        self.shelf_life = shelf_life
        self.quantity = quantity
        self.unit_calories = unit_calories
        self.purchase_date = purchase_date
        self.user_id = user_id
