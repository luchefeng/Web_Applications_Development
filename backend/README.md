# My Web Project - Backend
2025.2.9
#instructures

my_flask_project/
│
├── .env
│
├── app2.py
│
├── models2.py
│
├── README.md
│
├── requirements.txt
│
├── routes2_users.py
│
├── routes2_recipes.py
│
├── routes2_calorie.py
│
└── templates/
    └── calorie/
        ├── calculator.html
        └── educational.html
        └── intake.html
        └── management.html
        └── set_goal.html
        └── weight.html
    └── recipes/
        ├── index.html
        └── recipe.html
    └── users/
        ├── dashboard.html
        ├── operations.html
        └── profile.html
    

#一些说明：本次实现的功能是将“卡路里管理模块”添加进来，包括
    1.“用户卡路里目标设置模块”
        实现了获取用户的个人信息，根据这些信息计算（计算标准：BMR+TDEE)得到每日卡路里目标（大卡），并存入放入数据库flaskdb的calorie_goal表中。
            #####待改进之处：将用户的这些个人信息存入数据库中，而不是仅仅在此处用于计算#####
    “科普栏”
        实现了让一些科普知识滑动展示
            #####待改进之处：丰富科普知识的内容和严谨度#####
    “卡路里计算器”
        #####本模块计算方法不严谨，需配合后续食材信息录入才能更严谨地计算，先不做要求#####
    “卡路里摄入记录”
        #####同“卡路里计算器”模块，不过摄入记录可以正常存入数据库flaskdb的calorie_intake表中#####
    “体重记录仪”
        实现了日期和体重的记录，并能将记录正常存入数据库flaskdb的weight_record表中
            #####待改进之处：向用户展示更全面、更科学的身体指标，包括但不限于体脂率、BMR、体重等。
以上功能需在用户登录后可查看；本次将数据库flaskdb的密码一并上传在.env文件中
待改进之处用次“#####”标注

#补充说明：
    本次使用的代码，根据上一次branch-with_vite的内容进行了调整（此处仅说明后端），调整内容包括：
在app2.py中加入cors，然后根据“卡路里管理模块”的需要，在app2.py中注册了蓝图，models2.py中增加了数据库中的表的模型，以及新增route2_calorie.py的模块路由部分。

需要注意的是，观察对比发现，原本的route2.users.py因前后端注册连通的需要，进行了更改，但始终没能解决的Unsupported Media Type Did not attempt to load JSON data because the request Content-Type was not 'application/json'.报错信息。
因此“卡路里管理模块”还是基于未连通前后端时的route2.users.py文件。

#正文结束，以下是我的不严肃碎碎念
疑点：
1.若采用注册连通的前后端文件，当我从前端的地址访问时，当点击用户注册时，数据可以正常录入数据库中；但当点击用户登录时，页面无反应，无法进入用户仪表盘。是仪表盘还没制作使得页面无法跳转还是我的后端有问题？
2.若采用注册连通的前后端文件，当我从后端的地址访问时（端口号5000），在用户登录界面，点击登录，会出现Unsupported Media Type的报错，虽然知道是格式不对，但是尝试添加一下Login.vue的Content-Type为application/json，但还是报这个错。
我不太清楚应该怎么调整了。
3.所以我先将route2_users.py改回了原来没连通的状态，去设计卡路里模块的后端。如果有眉目，我会及时修改任何有关的文件的。