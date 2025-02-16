# Vue 3 + Vite

前端技术栈 vue3 + vite(脚手架) + axios(连通前后端) + vue-router(前端路由) + vuex（状态管理）。
直接使用了Ant Design Vue中的一些组件(https://www.antdv.com/docs/vue/introduce-cn) 。
直接尝试连通前后端会失败，所以需要通过Flask-CORS解决跨端问题。 

## 目前实现的

- 连通后端完成注册登录。
- 更改页面布局，使其更加合理（在顶部栏右侧添加登录与注册选项，样式参考(https://www.musicca.com/zh)
- 修改初始页面主体
- 更改登录页面样式

## 下一步要实现的

- 进一步修改初始页面

- 在注册之前让用户选择模式（关注卡路里与否），并以基础的basic layout为基础，构建两个版本的layout，在选择了对应模式的用户登录后切入对应的basiclayout和对应的仪表盘

## 下下步要实现的


## 需要后端的部分

- 在用户的数据模型中新增选择是否关注卡路里这一项
