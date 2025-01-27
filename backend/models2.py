from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy( ) # 创建SQLAlchemy实例

class User(db.Model):
    '''用户模型'''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自動增長
    username = db.Column(db.String(255), unique=True, nullable=False)  # 用户名
    email = db.Column(db.String(255), unique=True, nullable=False)  # 邮箱
    password_hash = db.Column(db.String(255), nullable=False)  # 密码哈希
    calorie_goal = db.Column(db.Integer, default=2000)  # 卡路里目标


    def set_password(self, password):
        '''设置密码'''
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        '''检查密码'''
        return check_password_hash(self.password_hash, password)


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


