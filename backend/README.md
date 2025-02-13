# My Web Project - Backend

#本版本实现的功能：
1.增添了用户登录时的验证码功能。

#说明：
对于前端输入验证码时，无法登入，只是出现“錯誤請求：請檢查您的輸入”的解决办法：
    在 Login.vue 的 onMounted 句子中调用 fetchCaptcha，确保页面加载时自动获取验证码。
    然后在用戶点击登录按钮，先验证验证码，再调用 login。