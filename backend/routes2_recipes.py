from flask import Blueprint, render_template, jsonify, request
from models2 import db, Recipes
from flask_login import current_user, login_required

recipes_bp = Blueprint('recipes', __name__) # 创建食谱蓝图

@recipes_bp.route('/') # 設置食谱视图路由
def index():
    '''食谱视图'''
    recipes = Recipes.query.all() # 查询所有食谱
    return render_template('recipes/dashboard.html', recipes=recipes)

@recipes_bp.route('/<int:id>') # 設置食谱详情视图路由
def recipe(id):
    '''食谱详情视图'''
    recipe = Recipes.query.get(id)# 查询食谱
    return render_template('recipes/recipe.html', recipe=recipe)

@recipes_bp.route('/list', methods=['GET'])
@login_required
def get_recipes():
    """获取菜谱列表"""
    try:
        recipes = Recipes.query.all()
        recipes_list = [{
            'id': recipe.id,
            'title': recipe.title,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'user_id': recipe.user_id
        } for recipe in recipes]
        return jsonify(recipes_list), 200
    except Exception as e:
        return jsonify({'message': '获取菜谱失败', 'error': str(e)}), 400

@recipes_bp.route('/add', methods=['POST'])
@login_required
def add_recipe():
    try:
        data = request.json
        new_recipe = Recipes(
            title=data['title'],
            ingredients=data['ingredients'],
            instructions=data['instructions'],
            user_id=current_user.id
        )
        db.session.add(new_recipe)
        db.session.commit()

        # 返回新创建的菜谱数据
        return jsonify({
            'message': '菜谱添加成功！',
            'recipe': {
                'id': new_recipe.id,
                'title': new_recipe.title,
                'ingredients': new_recipe.ingredients,
                'instructions': new_recipe.instructions
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '添加失败', 'error': str(e)}), 400