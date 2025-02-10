from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from models2 import db, User, CalorieGoal, CalorieIntake, WeightRecord
from werkzeug.security import generate_password_hash, check_password_hash

calorie_bp = Blueprint('calorie', __name__)

# 卡路里管理模块主页
@calorie_bp.route('/calorie_management')
@login_required
def calorie_management():
    return render_template('calorie/management.html', user=current_user)

# 用户卡路里目标设置模块
@calorie_bp.route('/set_calorie_goal', methods=['GET', 'POST'])
@login_required
def set_calorie_goal():
    if request.method == 'POST':
        data = request.form
        gender = data.get('gender')
        age = int(data.get('age'))
        height = float(data.get('height'))
        current_weight = float(data.get('current_weight'))
        target_weight = float(data.get('target_weight'))
        activity_level = data.get('activity_level')
        timeframe = int(data.get('timeframe'))

        if not gender or not age or not height or not current_weight or not target_weight or not timeframe or not activity_level:
            flash('所有字段均为必填项。')
            return redirect(url_for('calorie.set_calorie_goal'))

        bmr = calculate_bmr(gender, current_weight, height, age)
        tdee = calculate_tdee(bmr, activity_level)
        total_calorie_deficit = (current_weight - target_weight) * 7700
        daily_calorie_deficit = total_calorie_deficit / timeframe
        daily_calorie_goal = tdee - daily_calorie_deficit

        if daily_calorie_goal < 1200:  # 添加警告：每日攝入卡路里過低
            flash(f'警告：每日卡路里目标（{daily_calorie_goal} 大卡）過低，可能不健康。請調整減重計劃。')
        else:
            calorie_goal = CalorieGoal(user_id=current_user.id, goal=daily_calorie_goal)
            db.session.add(calorie_goal)
            db.session.commit()
            flash(f'卡路里目标设置成功！每日卡路里目标：{daily_calorie_goal} 大卡')

        return redirect(url_for('calorie.set_calorie_goal'))

    return render_template('calorie/set_goal.html', user=current_user)

def calculate_bmr(gender, weight, height, age):
    if gender == '男':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def calculate_tdee(bmr, activity_level):
    activity_multiplier = {
        '久坐': 1.2,
        '轻度活动': 1.375,
        '中度活动': 1.55,
        '高度活动': 1.725,
        '极度活动': 1.9
    }
    return bmr * activity_multiplier.get(activity_level, 1.375)

# 科普栏
@calorie_bp.route('/educational')
@login_required
def educational():
    content = {
        'definition': '卡路里是能量的单位，用来衡量食物中的能量含量。',
        'tips': '减肥不能操之过急，健康的减重速度是每周0.5到1公斤。',
        'daily_message': '每日标语：保持积极心态，健康生活。',
        'obesity_risks': '过度肥胖可能导致心血管疾病、糖尿病和高血压等健康问题。'
    }
    return render_template('calorie/educational.html', content=content, user=current_user)

# 卡路里计算器
@calorie_bp.route('/calorie_calculator', methods=['GET', 'POST'])
@login_required
def calorie_calculator():
    if request.method == 'POST':
        data = request.form
        food_item = data.get('food_item')
        serving_size = data.get('serving_size')
        meal_time = data.get('meal_time')

        if not food_item or not serving_size or not meal_time:
            flash('所有字段均为必填项。')
            return redirect(url_for('calorie.calorie_calculator'))

        calorie_estimate = estimate_calories(food_item, serving_size)
        recipes = recommend_recipes(food_item, serving_size)

        flash(f'卡路里估算：{calorie_estimate} 卡路里')
        flash(f'推荐菜谱：{", ".join([recipe["name"] for recipe in recipes])}')
        return redirect(url_for('calorie.calorie_calculator'))

    return render_template('calorie/calculator.html', user=current_user)

def estimate_calories(food_item, serving_size):
    return 100 * serving_size

def recommend_recipes(food_item, serving_size):
    recipes = [
        {'name': '简单炒饭', 'calories': 300},
        {'name': '清炒蔬菜', 'calories': 150}
    ]
    return recipes

# 卡路里摄入记录
@calorie_bp.route('/record_calorie_intake', methods=['GET', 'POST'])
@login_required
def record_calorie_intake():
    if request.method == 'POST':
        data = request.form
        intake = data.get('intake')
        meal_time = data.get('meal_time')
        food_item = data.get('food_item')

        if not intake or not meal_time or not food_item:
            flash('所有字段均为必填项。')
            return redirect(url_for('calorie.record_calorie_intake'))

        calorie_intake = CalorieIntake(user_id=current_user.id, intake=intake, meal_time=meal_time, food_item=food_item)
        db.session.add(calorie_intake)
        db.session.commit()

        flash('卡路里摄入记录成功！')
        return redirect(url_for('calorie.record_calorie_intake'))

    return render_template('calorie/intake.html', user=current_user)

# 体重记录仪
@calorie_bp.route('/record_weight', methods=['GET', 'POST'])
@login_required
def record_weight():
    if request.method == 'POST':
        data = request.form
        weight = data.get('weight')
        date = data.get('date')

        if not weight or not date:
            flash('体重和日期是必填项。')
            return redirect(url_for('calorie.record_weight'))

        weight_record = WeightRecord(user_id=current_user.id, weight=weight, date=date)
        db.session.add(weight_record)
        db.session.commit()

        weight_records = WeightRecord.query.filter_by(user_id=current_user.id).order_by(WeightRecord.date).all()
        if len(weight_records) > 1:
            weight_loss_rate = calculate_weekly_weight_loss(weight_records)
        else:
            weight_loss_rate = None

        flash(f'体重记录成功！每周体重下降速度：{weight_loss_rate} kg/周' if weight_loss_rate else '体重记录成功！')
        return redirect(url_for('calorie.record_weight'))

    return render_template('calorie/weight.html', user=current_user)

def calculate_weekly_weight_loss(weight_records):
    initial_weight = weight_records[0].weight
    latest_weight = weight_records[-1].weight
    weeks = (weight_records[-1].date - weight_records[0].date).days / 7
    weight_loss_rate = (initial_weight - latest_weight) / weeks
    return weight_loss_rate
