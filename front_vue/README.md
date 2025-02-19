# Vue 3 + Vite

前端技术栈 vue3 + vite(脚手架) + axios(连通前后端) + vue-router(前端路由) + vuex（状态管理）。

直接使用了Ant Design Vue中的一些组件(https://www.antdv.com/docs/vue/introduce-cn) 。

直接尝试连通前后端会失败，所以需要通过Flask-CORS解决跨端问题。

## 目前实现的

- 连通后端完成注册登录。
- 更改页面布局，使其更加合理（在顶部栏右侧添加登录与注册选项，样式参考(https://www.musicca.com/zh)
- 修改初始页面主体
- 更改登录页面样式
- 更改了登录后的顶栏，新增登出键（但是目前点击登出键后，会出现304的状态码，不会自动跳转首页，需要手动刷新
- 将食品柜页面进行了修改，原Ingredient_Management.vue文件中的内容移动至组件Ingredient_Add.vue中，修改了Ingredient_management.vue中的内容，使得食品柜中的食品可以展示(展示食品柜的组件为Ingredient_Show.vue)
！但是，目前样式仅为测试，之后还会修改
- 添加Ingredient_Recomend.vue，实现推荐食品的功能
! 目前尚未与后端联通
- 在BasicLayout_calorie.vue中详细进行了CORS的设置，使得前端可以正常与后端进行通信
- 更改layout，使得点击头像跳转个人资料页，并新增其他内容
- 更改了BasicLayout_calorie.vue和BasicLayout_coo.vue，但是切换暂时还存在问题（新建了test1用于测试此问题）

## 下一步要实现的

- debug顶栏更改的问题

## 下下步要实现的

- 进一步美化各个页面

## 需要后端的部分

- 后端在登出时候的重定向需要完善（AI原话：问题原因：
原代码使用 redirect() 进行重定向，这会返回 302 状态码
前端是通过 AJAX 调用登出接口，不需要后端进行重定向
302 重定向会导致前端的 Promise 无法正确处理响应
修改后：
直接返回 JSON 响应和 200 状态码
清理所有相关的会话数据
让前端控制登出后的页面跳转”）
