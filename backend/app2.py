from flask import Flask, render_template
from models2 import db, User, Recipes, Article,UserProfile
from routes2_users import users_bp
from routes2_recipes import recipes_bp
from routes2_calorie import calorie_bp
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_cors import CORS  ####### 导入 CORS //新增
import os #与操作系统交互

load_dotenv() # 加载.env文件

app = Flask(__name__) # 创建Flask应用
#CORS(app)  # 配置 CORS（跨源资源共享）//新增
CORS(app, supports_credentials=True)#使浏览器允许跨域的登录请求发送Cookie。

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') # 配置MySQL数据库
# 检查是否成功加载了 DATABASE_URL
if not app.config['SQLALCHEMY_DATABASE_URI']:
    raise RuntimeError("DATABASE_URL is not set in the environment variables.")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的跟踪

db.init_app(app)  # 初始化数据库

app.register_blueprint(users_bp, url_prefix='/users') # 注册用戶蓝图
app.register_blueprint(recipes_bp, url_prefix='/recipes') # 注册食谱蓝图
app.register_blueprint(calorie_bp, url_prefix='/calorie') # 注册卡路里蓝图

login_manager = LoginManager()  # 初始化 LoginManager
login_manager.init_app(app)  # 將其綁定到 Flask 應用
login_manager.login_view = 'users.login'  # 設置登錄視圖

with app.app_context():
    db.create_all() # 创建所有表

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True) # 运行应用

