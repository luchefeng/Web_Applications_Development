# My Web Project - Backend

#instructures

my_flask_project/
│
├── app2.py
│
├── models2.py
│
├── routes2_users.py
│
├── routes2_recipes.py
│
├── .env
│
├── .gitignore
└── templates/
    └── users/
        ├── index.html
        └── user.html
    └── recipes/
        ├── index.html
        └── recipe.html

#一些说明：本次主要是实现了在前端网页输入用户注册信息时，数据能够顺利传入后端并存入数据库。
#但还需要改进的地方是，
第一，当用户注册成功后，应该显示注册成功，然后跳转到登录页面，而不是什么提示都没有。
第二，如果用户注册时，用户名或者邮箱已经存在，应该提示用户并拒绝将其插入数据库，目前我的这个就算重名了还是会插进数据库，也会占数据库的主键id数目，但是它不会在数据库里显示
     比如第一个用户注册为first，然后第二个用户注册为first，那么第二个用户注册成功后，数据库里会有两个id，但是只有一个用户的信息。当第三个用户注册时，数据库里会有id=1和id=3
     也就是重复注册以后，重复的用户名会占用数据库的id，但是不会在数据库里显示。
