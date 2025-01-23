from flask  import Blueprint, render_template
from models2 import Recipes

recipes_bp = Blueprint('recipes', __name__) # 创建食谱蓝图

@recipes_bp.route('/') # 設置食谱视图路由
def index():
    '''食谱视图'''
    recipes = Recipes.query.all() # 查询所有食谱
    return render_template('recipes/index.html', recipes=recipes)

@recipes_bp.route('/<int:id>') # 設置食谱详情视图路由
def recipe(id):
    '''食谱详情视图'''
    recipe = Recipes.query.get(id)# 查询食谱
    return render_template('recipes/recipe.html', recipe=recipe)