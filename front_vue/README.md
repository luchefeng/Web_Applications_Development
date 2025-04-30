# Vue 3 + Vite

前端技术栈 vue3 + vite(脚手架) + axios(连通前后端) + vue-router(前端路由) + vuex（状态管理）。

直接使用了Ant Design Vue中的一些组件(https://www.antdv.com/docs/vue/introduce-cn) 。

直接尝试连通前后端会失败，所以需要通过Flask-CORS解决跨端问题。

## 4.29更新

### 已经实现的

- 更改首页解说词
- 更改卡路里显示小数位数
- 修改，使得未登录时点击“导航”回到首页

### 等待实现的

- 实现连通前后端的“记住我”和“忘记密码”
- 更改注册界面的版本选择逻辑
- 疑似存在刷新网页直接退出登录的bug，等待修复
- 更改卡路里页面的前端排版，使其能查看历史卡路里、体重变化
- 连通卡路里界面的食材和卡路里关联

## 3月之前实现的

- 连通后端完成注册登录。
- 更改页面布局，使其更加合理（在顶部栏右侧添加登录与注册选项，样式参考(https://www.musicca.com/zh)
- 修改初始页面主体
- 更改登录页面样式
- 更改了登录后的顶栏，新增登出键（但是目前点击登出键后，会出现304的状态码，不会自动跳转首页，需要手动刷新
- 将食品柜页面进行了修改，原Ingredient_Management.vue文件中的内容移动至组件Ingredient_Add.vue中，修改了Ingredient_management.vue中的内容，使得食品柜中的食品可以展示(展示食品柜的组件为Ingredient_Show.vue)
！但是，目前样式仅为测试，之后还会修改
- 添加Ingredient_Recomend.vue，实现推荐食品的功能
- 目前尚未与后端联通
- 在BasicLayout_calorie.vue中详细进行了CORS的设置，使得前端可以正常与后端进行通信
- 更改layout，使得点击头像跳转个人资料页，并新增其他内容
- 更改了BasicLayout_calorie.vue和BasicLayout_coo.vue，但是切换暂时还存在问题（新建了test1用于测试此问题）
- debug顶栏更改的问题
- 注册时可以选择不同的版本
