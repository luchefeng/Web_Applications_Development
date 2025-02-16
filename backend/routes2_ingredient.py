from flask import Blueprint, request, jsonify
from models2 import db, Ingredient
from flask_login import current_user, login_required
from datetime import datetime

ingredient_bp = Blueprint('ingredient', __name__)

def convert_quantity_to_grams(food_name, food_quantity):
    conversion_factors = {
        '白菜': {'1顆': 500, '半顆': 250},
        '番茄': {'1個': 150, '2個': 300},
        # 添加更多食材及其換算比例
    }
    if 'g' in food_quantity:
        return int(food_quantity.replace('g', ''))
    else:
        return conversion_factors.get(food_name, {}).get(food_quantity, 0)

@ingredient_bp.route('/add', methods=['POST'])
@login_required
def add_ingredient():
    try:
        data = request.json
        name = data.get('name')
        category = data.get('category')
        shelf_life = int(data.get('shelf_life'))
        quantity = data.get('quantity')
        unit_calories = float(data.get('unit_calories'))
        purchase_date = datetime.strptime(data.get('purchase_date'), '%Y-%m-%d')

        quantity_in_grams = convert_quantity_to_grams(name, quantity)

        new_ingredient = Ingredient(
            name=name,
            category=category,
            shelf_life=shelf_life,
            quantity=quantity_in_grams,
            unit_calories=unit_calories,
            purchase_date=purchase_date,
            user_id=current_user.id
        )

        db.session.add(new_ingredient)
        db.session.commit()
        return jsonify({'message': 'Ingredient added successfully!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to add ingredient', 'error': str(e)}), 400

@ingredient_bp.route('/get_all', methods=['GET'])
@login_required
def get_all_ingredients():
    ingredients = Ingredient.query.filter_by(user_id=current_user.id).all()
    result = []
    for ingredient in ingredients:
        ingredient_data = {
            'id': ingredient.id,
            'name': ingredient.name,
            'category': ingredient.category,
            'shelf_life': ingredient.shelf_life,
            'quantity': ingredient.quantity,
            'unit_calories': ingredient.unit_calories,
            'purchase_date': ingredient.purchase_date.strftime('%Y-%m-%d')
        }
        result.append(ingredient_data)

    return jsonify(result)

@ingredient_bp.route('/update/<int:id>', methods=['PUT'])
@login_required
def update_ingredient(id):
    ingredient = Ingredient.query.get(id)
    if not ingredient or ingredient.user_id != current_user.id:
        return jsonify({'message': 'Ingredient not found or not authorized!'}), 404

    data = request.json
    ingredient.name = data.get('name', ingredient.name)
    ingredient.category = data.get('category', ingredient.category)
    ingredient.shelf_life = int(data.get('shelf_life', ingredient.shelf_life))
    ingredient.quantity = convert_quantity_to_grams(ingredient.name, data.get('quantity', ingredient.quantity))
    ingredient.unit_calories = float(data.get('unit_calories', ingredient.unit_calories))
    ingredient.purchase_date = datetime.strptime(data.get('purchase_date', ingredient.purchase_date.strftime('%Y-%m-%d')))

    db.session.commit()

    return jsonify({'message': 'Ingredient updated successfully!'})

@ingredient_bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_ingredient(id):
    ingredient = Ingredient.query.get(id)
    if not ingredient or ingredient.user_id != current_user.id:
        return jsonify({'message': 'Ingredient not found or not authorized!'}), 404

    db.session.delete(ingredient)
    db.session.commit()

    return jsonify({'message': 'Ingredient deleted successfully!'})
