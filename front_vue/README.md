# Vue 3 + Vite

前端技术栈 vue3 + vite(脚手架) + axios(连通前后端) + vue-router(前端路由) + vuex（状态管理）。
直接使用了Ant Design Vue中的一些组件(https://www.antdv.com/docs/vue/introduce-cn) 。
直接尝试连通前后端会失败，所以需要通过Flask-CORS解决跨端问题。 

目前实现的：连通后端完成注册。
下一步要实现的：

1. 更改页面布局，使其更加合理（在顶部栏右侧添加登录与注册选项，样式参考(https://www.musicca.com/zh)
2. 修改初始页面主体
3. 在注册之前让用户选择模式（关注卡路里与否）

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).
