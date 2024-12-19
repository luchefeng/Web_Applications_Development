from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Recipe, Article
from . import db

routes = Blueprint('routes', __name__)

# 用户注册
@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': '用户已存在'}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201

# 用户登录
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({'message': '登录成功'}), 200
    return jsonify({'message': '用户名或密码错误'}), 401

# 用户登出
@routes.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': '登出成功'}), 200

# 获取用户信息
@routes.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'calorie_goal': current_user.calorie_goal
    }), 200

# 提交食谱
@routes.route('/recipes', methods=['POST'])
@login_required
def post_recipe():
    data = request.get_json()
    title = data.get('title')
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')

    new_recipe = Recipe(title=title, ingredients=ingredients, instructions=instructions, user_id=current_user.id)
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({'message': '食谱已提交'}), 201

# 获取食谱推荐
@routes.route('/recipes/recommendations', methods=['GET'])
@login_required
def get_recommendations():
    calorie_goal = current_user.calorie_goal
    recipes = Recipe.query.filter(Recipe.calories <= calorie_goal).all()
    return jsonify([{'title': recipe.title, 'ingredients': recipe.ingredients} for recipe in recipes]), 200

# 获取文章列表
@routes.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([{'title': article.title, 'content': article.content} for article in articles]), 200

# 获取单个文章
@routes.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({'title': article.title, 'content': article.content}), 200