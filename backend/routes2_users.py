from flask  import Blueprint, render_template
from models2 import User

users_bp = Blueprint('users', __name__) # 创建用戶蓝图

@users_bp.route('/') # 設置用戶视图路由
def index():
    '''用戶视图'''
    users = User.query.all() # 查询所有用戶
    return render_template('users/index.html', users=users)

@users_bp.route('/<int:id>') # 設置用戶详情视图路由
def user(id):
    '''用戶详情视图'''
    user = User.query.get(id) # 查询用戶
    return render_template('users/user.html', user=user)