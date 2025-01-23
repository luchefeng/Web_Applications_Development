from flask import Flask
from models2 import db, User, Recipes, Article
from routes2_users import users_bp
from routes2_recipes import recipes_bp
from dotenv import load_dotenv
import os #这个模块提供了与操作系统交互的功能，包括文件和目录的操作、环境变量的访问等等

load_dotenv() # 加载.env文件

app = Flask(__name__) # 创建Flask应用
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') # 配置MySQL数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的跟踪

db.init_app(app)  # 初始化数据库

app.register_blueprint(users_bp, url_prefix='/users') # 注册用戶蓝图
app.register_blueprint(recipes_bp, url_prefix='/recipes') # 注册食谱蓝图

with app.app_context():
    db.create_all() # 创建所有表

if __name__ == '__main__':
    app.run(debug=True) # 运行应用