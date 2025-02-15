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
        daily_calorie_goal = tdee - daily_calorie_deficit

        if daily_calorie_goal < 1200:
            return jsonify({'message': f'警告：每日卡路里目标（{daily_calorie_goal} 大卡）过低，可能不健康。请调整减重计划。'}), 400

        calorie_goal = CalorieGoal(user_id=current_user.id, goal=daily_calorie_goal)
        db.session.add(calorie_goal)
        db.session.commit()

        return jsonify({'message': '卡路里目标设置成功！', 'data': {'daily_calorie_goal': daily_calorie_goal}}), 200
    except Exception as e:
        print('Error in set_calorie_goal:', traceback.format_exc())  # 打印详细的错误堆栈信息
        return jsonify({'message': '設置卡路里目標失敗，請稍後再試。'}), 500

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
