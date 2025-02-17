# My Web Project - Backend

#本版本关注“卡路里管理”模块的开发：
本次更新內容：
1.解決食材无法添加进数据库的问题
    核心语句：    await axios.post('http://localhost:5000/ingredient/add', data, { withCredentials: true });
    该语句确认前端方法为POST，以避免405错误
    相关更改文件：front_vue/src/views/Ingredient_Management.vue

2.将后端用户界面各路由更改为可接收与发送json数据格式的形式
    更改了的路由：logout, dashboard, user_info, delete_account, reset_password 
    相关更改文件: backend/routes2_users.py

3.在更改“2”以后，原本已在前端完成的登出按钮消失，调整了一些文件内容，现已恢复登出功能
    相关更改文件:front_vue/src/App.vue，以及front_vue/src/store/index.js


下一步设计思路：
1.在用户的数据模型中新增选择是否关注卡路里这一项
2.完善食品柜逻辑，使其更合理
3.设计卡路里摄入记录、体重记录仪
4.因为该API和卡路里管理模块有交织的地方，所以两个模块可能会同时进行


本模块和前端有关的东西有：
1.完善各模块界面设计