# 定义与 `ingredients` 表交互的类和方法
#用于封装与数据库表 ingredients 的交互逻辑
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

class Ingredient(db.Model):
    '''
    数据库模型：食材信息
    '''
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
        '''
        将食材信息转换为字典格式，便于返回 JSON 数据
        '''
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
"""