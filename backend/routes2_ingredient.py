from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models2 import db, Ingredient
import logging
import requests
import os

ingredient_bp = Blueprint('ingredient_bp', __name__, url_prefix='/ingredient')

@ingredient_bp.route('/search_usda', methods=['GET'])
@login_required
def search_usda():
    try:
        query = request.args.get('query')
        if not query:
            return jsonify({'message': 'No query provided'}), 400

        # 读取.env环境变量里的USDA_API_KEY
        usda_api_key = os.getenv('USDA_API_KEY')
        if not usda_api_key:
            return jsonify({'message': 'USDA API key not set on server'}), 500

        usda_url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={query}&api_key={usda_api_key}'
        response = requests.get(usda_url)
        response.raise_for_status()

        result = response.json()

        # 解析卡路里
        if not result.get('foods'):
            return jsonify({'message': 'No food found'}), 404

        food = result['foods'][0]  # 取第一个结果
        description = food.get('description', 'Unknown food')
        nutrients = food.get('foodNutrients', [])

        unit_calories = None
        for nutrient in nutrients:
            if nutrient.get('nutrientName') == 'Energy' and nutrient.get('unitName') == 'KCAL':
                unit_calories = nutrient.get('value')
                break

        if unit_calories is None:
            return jsonify({'message': 'No calorie information found'}), 404

        return jsonify({
            'name': description,
            'unit_calories': unit_calories
        }), 200

    except requests.exceptions.RequestException as e:
        return jsonify({'message': 'USDA API request failed', 'error': str(e)}), 500
    except Exception as e:
        return jsonify({'message': 'Server error', 'error': str(e)}), 500

# 添加食材
@ingredient_bp.route('/add', methods=['POST'])
@login_required
def add_ingredient():
    data = request.get_json()
    user_id = current_user.id
    name = data.get('name')
    category = data.get('category')
    shelf_life = data.get('shelf_life')
    quantity = data.get('quantity')
    unit_calories = data.get('unit_calories')
    purchase_date = data.get('purchase_date')

    new_ingredient = Ingredient(
        user_id=user_id,
        name=name,
        category=category,
        shelf_life=shelf_life,
        quantity=quantity,
        unit_calories=unit_calories,
        purchase_date=purchase_date
    )

    try:
        db.session.add(new_ingredient)
        db.session.commit()
        # 返回新添加的食材信息
        return jsonify({
            'message': '食材添加成功',
            'ingredient': {
                'id': new_ingredient.id,
                'name': new_ingredient.name,
                'category': new_ingredient.category,
                'shelf_life': new_ingredient.shelf_life,
                'quantity': new_ingredient.quantity,
                'unit_calories': new_ingredient.unit_calories,
                'purchase_date': new_ingredient.purchase_date.strftime('%Y-%m-%d')
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': '食材添加失败', 'error': str(e)}), 400

# 获取用户的所有食材
@ingredient_bp.route('/get_all', methods=['GET'])
@login_required
def get_all_ingredients():
    try:
        user_id = current_user.id
        logging.info(f"当前用户 ID: {user_id}")
        ingredients = Ingredient.query.filter_by(user_id=user_id).all()
        logging.info(f"查询到的食材数量: {len(ingredients)}")
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append({
                'id': ingredient.id,
                'name': ingredient.name,
                'category': ingredient.category,
                'shelf_life': ingredient.shelf_life,
                'quantity': ingredient.quantity,
                'unit_calories': ingredient.unit_calories,
                'purchase_date': ingredient.purchase_date.strftime('%Y-%m-%d')
            })
        return jsonify(ingredient_list), 200
    except Exception as e:
        logging.error(f"获取食材列表时出现错误: {str(e)}")
        return jsonify({"error": "获取食材列表时出现错误"}), 500

# 更新食材信息
@ingredient_bp.route('/update/<int:ingredient_id>', methods=['PUT'])
@login_required
def update_ingredient(ingredient_id):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return jsonify({'message': 'Ingredient not found.'}), 404

        data = request.json

        # 更新食材信息
        ingredient.name = data.get('name', ingredient.name)
        ingredient.category = data.get('category', ingredient.category)
        ingredient.shelf_life = data.get('shelf_life', ingredient.shelf_life)
        ingredient.quantity = data.get('quantity', ingredient.quantity)
        ingredient.unit_calories = data.get('unit_calories', ingredient.unit_calories)
        ingredient.purchase_date = datetime.strptime(data.get('purchase_date'), '%Y-%m-%d') if data.get(
            'purchase_date') else ingredient.purchase_date

        db.session.commit()
        return jsonify({'message': 'Ingredient updated successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to update ingredient', 'error': str(e)}), 400

# 删除食材
@ingredient_bp.route('/delete/<int:ingredient_id>', methods=['DELETE'])
@login_required
def delete_ingredient(ingredient_id):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return jsonify({'message': 'Ingredient not found.'}), 404

        db.session.delete(ingredient)
        db.session.commit()
        return jsonify({'message': 'Ingredient deleted successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to delete ingredient', 'error': str(e)}), 400

# 转换数量为克（根据某些条件转换）
@ingredient_bp.route('/convert', methods=['POST'])
@login_required
def convert_quantity_to_grams():
    try:
        data = request.json
        ingredient_id = data.get('ingredient_id')
        new_quantity_in_grams = data.get('new_quantity_in_grams')

        ingredient = Ingredient.query.get(ingredient_id)
        if not ingredient:
            return jsonify({'message': 'Ingredient not found.'}), 404

        ingredient.quantity = new_quantity_in_grams
        db.session.commit()

        return jsonify({'message': 'Ingredient quantity converted successfully!', 'ingredient': {
            'name': ingredient.name,
            'quantity': ingredient.quantity
        }}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to convert quantity', 'error': str(e)}), 400