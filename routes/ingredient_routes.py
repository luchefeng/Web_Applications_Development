# 食材管理模块的路由定义
#定义路由，将 HTTP 请求转发到模型中的对应方法

from flask import Blueprint, request, jsonify, session,redirect, url_for,flash
#from models.ingredient_model import Ingredient, db
#from app import Ingredient, db
from utils.db import db
from models.ingredient_model import Ingredient
from flask_login import current_user
import logging

ingredient_bp = Blueprint('ingredient_bp', __name__, url_prefix='/ingredients')

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@ingredient_bp.before_request
def check_login():
    """
    验证用户是否登录。
    未登录时拒绝访问核心接口。
    """
    # demo 接口不需要登录
    if request.endpoint != 'ingredient_bp.get_sample_ingredients' and not current_user.is_authenticated:
        logger.error(f"未登录用户尝试访问：{request.endpoint}")  # 记录日志
        return jsonify({"error": "Unauthorized. Please log in first."}), 401
@ingredient_bp.route('/demo', methods=['GET'])
def get_sample_ingredients():
    """
    提供示例数据供未登录用户预览。
    """
    sample_ingredients = [
        {"name": "Tomato", "quantity": 0, "unit": "kg"},
        {"name": "Potato", "quantity": 0, "unit": "kg"}
    ]
    return jsonify(sample_ingredients), 200

@ingredient_bp.route('/', methods=['GET'])
def get_all_ingredients():
    """
    查询登录用户的所有食材信息。
    """
    ingredients = Ingredient.query.all()
    return jsonify([ingredient.to_dict() for ingredient in ingredients]), 200

@ingredient_bp.route('/add', methods=['POST'])
def add_ingredient():
    """
    添加新食材。
    """
    data = request.get_json()
    try:
        ingredient = Ingredient(
            name=data['name'],
            quantity=data.get('quantity', 0),
            unit=data['unit'],
            calories=data.get('calories'),
            expiry_date=data.get('expiry_date'),
        )
        db.session.add(ingredient)
        db.session.commit()
        flash(f"食材 '{ingredient.name}' 添加成功！", "success")
        return redirect(url_for('ingredient.list'))
        #logger.info(f"新食材添加成功：{ingredient.name}")  # 记录日志
        #return jsonify({"message": "Ingredient added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        flash(f"添加食材时出错：{str(e)}", "error")
        return redirect(url_for('ingredient.list'))
        #logger.error(f"添加食材时出错：{str(e)}")  # 记录日志
        #return jsonify({"error": str(e)}), 400

@ingredient_bp.route('/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    """
    更新现有食材信息。
    """
    data = request.get_json()
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        flash("食材未找到", "error")
        return redirect(url_for('ingredient.list'))
        #return jsonify({"error": "Ingredient not found"}), 404

    try:
        ingredient.name = data.get('name', ingredient.name)
        ingredient.quantity = data.get('quantity', ingredient.quantity)
        ingredient.unit = data.get('unit', ingredient.unit)
        ingredient.calories = data.get('calories', ingredient.calories)
        ingredient.expiry_date = data.get('expiry_date', ingredient.expiry_date)
        db.session.commit()
        flash(f"食材 '{ingredient.name}' 更新成功！", "success")
        logger.info(f"食材更新成功：{ingredient.name}")  # 记录日志
        return redirect(url_for('ingredient.list'))
        #return jsonify({"message": "Ingredient updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        flash(f"更新食材时出错：{str(e)}", "error")
        logger.error(f" 更新食材时出错：{str(e)}")  # 记录日志
        return redirect(url_for('ingredient.list'))
        #return jsonify({"error": str(e)}), 400

@ingredient_bp.route('/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    """
    删除指定食材。
    """
    ingredient = Ingredient.query.get(ingredient_id)
    if not ingredient:
        flash("食材未找到", "error")
        return redirect(url_for('ingredient.list'))
        #return jsonify({"error": "Ingredient not found"}), 404

    try:
        db.session.delete(ingredient)
        db.session.commit()
        flash(f"食材 '{ingredient.name}' 删除成功！", "success")
        logger.info(f"食材删除成功：{ingredient.name}")  # 记录日志
        return redirect(url_for('ingredient.list'))
        #return jsonify({"message": "Ingredient deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        flash(f"删除食材时出错：{str(e)}", "error")
        logger.error(f"删除食材时出错：{str(e)}")  # 记录日志
        return redirect(url_for('ingredient.list'))
        #return jsonify({"error": str(e)}), 400
