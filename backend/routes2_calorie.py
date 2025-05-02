from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from models2 import db, CalorieGoal, CalorieIntake, WeightRecord
import traceback

calorie_bp = Blueprint('calorie', __name__)

# 卡路里管理模块主页
@calorie_bp.route('/calorie_management')
@login_required
def calorie_management():
    return jsonify({'message': '卡路里管理页面', 'data': {'user_id': current_user.id}}), 200

# 设置卡路里目标
@calorie_bp.route('/set_calorie_goal', methods=['POST'])
@login_required
def set_calorie_goal():
    try:
        data = request.json
        print('Received POST data:', data)  # 打印接收到的请求数据
        gender = data.get('gender')
        age = int(data.get('age'))
        height = float(data.get('height'))
        current_weight = float(data.get('current_weight'))
        target_weight = float(data.get('target_weight'))
        activity_level = data.get('activity_level')
        timeframe = int(data.get('timeframe'))

        if not gender or not age or not height or not current_weight or not target_weight or not timeframe or not activity_level:
            return jsonify({'message': '所有字段均为必填项。'}), 400

        bmr = calculate_bmr(gender, current_weight, height, age)
        tdee = calculate_tdee(bmr, activity_level)
        total_calorie_deficit = (current_weight - target_weight) * 7700
        daily_calorie_deficit = total_calorie_deficit / timeframe
        daily_calorie_goal = round(tdee - daily_calorie_deficit, 2)

        if daily_calorie_goal < 1200:
            return jsonify({'message': f'警告：每日卡路里目标（{daily_calorie_goal} 大卡）过低，可能不健康。请调整减重计划。'}), 400

        calorie_goal = CalorieGoal(user_id=current_user.id, goal=daily_calorie_goal)
        db.session.add(calorie_goal)
        db.session.commit()

        return jsonify({'message': '卡路里目标设置成功！', 'data': {'daily_calorie_goal': daily_calorie_goal}}), 200
    except Exception as e:
        print('Error in set_calorie_goal:', traceback.format_exc())  # 打印详细的错误堆栈信息
        return jsonify({'message': '設置卡路里目標失敗，請稍後再試。'}), 500

# 保存卡路里目标
@calorie_bp.route('/save_calorie_goal', methods=['POST'])
@login_required
def save_calorie_goal():
    try:
        data = request.json
        # Save all form data to the user's profile
        current_user.gender = data.get('gender')
        current_user.age = data.get('age')
        current_user.height = data.get('height')
        current_user.current_weight = data.get('current_weight')
        current_user.target_weight = data.get('target_weight')
        current_user.activity_level = data.get('activity_level')
        current_user.timeframe = data.get('timeframe')
        current_user.calorie_goal = data.get('calorie_goal')  # Make sure this is properly saved

        db.session.commit()
        return jsonify({'message': '卡路里目标保存成功！'}), 200
    except Exception as e:
        print('Error in save_calorie_goal:', traceback.format_exc())
        db.session.rollback()  # In case of error, rollback the session
        return jsonify({'message': '保存卡路里目标失败，请稍后再试。'}), 500

@calorie_bp.route('/get_calorie_goal', methods=['GET'])
@login_required
def get_calorie_goal():
    try:
        # Retrieve the user's saved calorie data
        saved_data = {
            'gender': current_user.gender,
            'age': current_user.age,
            'height': current_user.height,
            'current_weight': current_user.current_weight,
            'target_weight': current_user.target_weight,
            'activity_level': current_user.activity_level,
            'timeframe': current_user.timeframe,
            'calorie_goal': current_user.calorie_goal
        }
        return jsonify({'message': '获取保存的数据成功！', 'data': saved_data}), 200
    except Exception as e:
        print('Error in get_calorie_goal:', traceback.format_exc())
        return jsonify({'message': '获取保存的数据失败，请稍后再试。'}), 500

# 计算 BMR
def calculate_bmr(gender, weight, height, age):
    if gender == '男':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# 计算 TDEE
def calculate_tdee(bmr, activity_level):
    activity_multiplier = {
        '久坐': 1.2,
        '轻度活动': 1.375,
        '中度活动': 1.55,
        '高度活动': 1.725,
        '极度活动': 1.9
    }
    return bmr * activity_multiplier.get(activity_level, 1.375)

# 卡路里摄入记录
@calorie_bp.route('/record_calorie_intake', methods=['POST'])
@login_required
def record_calorie_intake():
    try:
        data = request.json
        intake = data.get('intake')
        meal_time = data.get('meal_time')
        food_item = data.get('food_item')

        if not intake or not meal_time or not food_item:
            return jsonify({'message': '所有字段均为必填项。'}), 400

        calorie_intake = CalorieIntake(user_id=current_user.id, intake=intake, meal_time=meal_time, food_item=food_item)
        db.session.add(calorie_intake)
        db.session.commit()

        return jsonify({'message': '卡路里摄入记录成功！'}), 200
    except Exception as e:
        print('Error in record_calorie_intake:', traceback.format_exc())
        return jsonify({'message': '記錄卡路里攝入失敗，請稍後再試。'}), 500

# 记录体重
@calorie_bp.route('/record_weight', methods=['POST'])
@login_required
def record_weight():
    try:
        data = request.json
        weight = data.get('weight')
        date = data.get('date')

        if not weight or not date:
            return jsonify({'message': '体重和日期是必填项。'}), 400

        weight_record = WeightRecord(user_id=current_user.id, weight=weight, date=date)
        db.session.add(weight_record)
        db.session.commit()

        return jsonify({'message': '体重记录成功！'}), 200
    except Exception as e:
        print('Error in record_weight:', traceback.format_exc())
        return jsonify({'message': '記錄體重失敗，請稍後再試。'}), 500

@calorie_bp.route('/calculate', methods=['POST'])
@login_required
def calculate_calories():
    try:
        data = request.json
        food_name = data.get('food_name')
        food_quantity = float(data.get('food_quantity'))
        meal_type = data.get('meal_type')

        # 根據食物名稱和數量計算卡路里
        calories = calculate_food_calories(food_name, food_quantity)

        # 根據計算出的卡路里範圍推薦簡單的菜譜
        recommended_recipes = recommend_recipes(calories, meal_type)

        return jsonify({'calories': calories, 'recommended_recipes': recommended_recipes}), 200
    except Exception as e:
        print('Error in calculate_calories:', traceback.format_exc())
        return jsonify({'message': '卡路里計算失敗，請稍後再試。'}), 500


def calculate_food_calories(food_name, food_quantity):
    # 這裡應該實現根據食物名稱和數量計算卡路里的邏輯
    # 例如從數據庫查詢或使用預定的數據
    calories_per_gram = {
        '蘋果': 0.52,  # 每克0.52卡路里
        '香蕉': 0.89,  # 每克0.89卡路里
        # 添加更多食物及其卡路里數據
    }
    return calories_per_gram.get(food_name, 0) * food_quantity


def recommend_recipes(calories, meal_type):
    # 這裡應該實現根據卡路里範圍和餐別推薦菜譜的邏輯
    # 例如從數據庫查詢或使用預定的菜譜數據
    recipes = [
        {'id': 1, 'name': '簡單蘋果沙拉'},
        {'id': 2, 'name': '香蕉燕麥粥'},
        # 添加更多簡單的菜譜
    ]
    # 篩選符合卡路里範圍和餐別的菜譜
    recommended_recipes = [recipe for recipe in recipes if recipe_fits_criteria(recipe, calories, meal_type)]
    return recommended_recipes


def recipe_fits_criteria(recipe, calories, meal_type):
    # 實現判斷菜譜是否符合卡路里範圍和餐別的邏輯
    return True  # 示例中所有菜譜都符合

@calorie_bp.route('/get_saved_data', methods=['GET'])
@login_required
def get_saved_data():
    try:
        # Retrieve the user's saved calorie data
        saved_data = {
            'gender': current_user.gender,
            'age': current_user.age,
            'height': current_user.height,
            'current_weight': current_user.current_weight,
            'target_weight': current_user.target_weight,
            'activity_level': current_user.activity_level,
            'timeframe': current_user.timeframe,
            'calorie_goal': current_user.calorie_goal
        }
        return jsonify({'message': '获取保存的数据成功！', 'data': saved_data}), 200
    except Exception as e:
        print('Error in get_saved_data:', traceback.format_exc())
        return jsonify({'message': '获取保存的数据失败，请稍后再试。'}), 500
