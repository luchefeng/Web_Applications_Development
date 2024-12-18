# 数据库连接与操作工具
#提供数据库连接工具，供其他模块使用

# 引入 SQLAlchemy 用于 ORM 操作
from flask_sqlalchemy import SQLAlchemy


# 创建全局数据库对象，供其他模块使用
db = SQLAlchemy()

