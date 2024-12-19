from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from utils.db import db


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
