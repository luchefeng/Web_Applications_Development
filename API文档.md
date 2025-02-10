# API 文档

## 基础信息
- 基础URL: `http://localhost:5000`
- 数据格式: JSON
- 认证方式: Session-based authentication

## 1. 用户管理 API

### 1.1 用户注册
- **请求路径**: `/users/register`
- **请求方法**: POST
- **请求参数**:
  ```json
  {
    "username": "string",     // 用户名
    "email": "string",       // 电子邮箱
    "password": "string",    // 密码
    "calorie_goal": "number" // 卡路里目标（可选）
  }
  ```
- **响应示例**:
  ```json
  // 成功
  {
    "message": "注册成功！请登录。",
    "status": 201
  }
  
  // 失败
  {
    "message": "用户名或邮箱已存在，请选择其他的",
    "status": 400
  }
  ```

### 1.2 用户登录
- **请求路径**: `/users/login`
- **请求方法**: POST
- **请求参数**:
  ```json
  {
    "username": "string",  // 用户名
    "password": "string"   // 密码
  }
  ```
- **响应示例**:
  ```json
  // 成功
  {
    "message": "登录成功！",
    "status": 200
  }
  
  // 失败
  {
    "message": "密码错误，请重试。",
    "status": 400
  }
  ```

### 1.3 用户登出
- **请求路径**: `/users/logout`
- **请求方法**: POST
- **请求参数**: 无
- **响应示例**:
  ```json
  {
    "message": "您已登出。",
    "status": 200
  }
  ```

### 1.4 删除账户
- **请求路径**: `/users/delete_account/<user_id>`
- **请求方法**: POST
- **请求参数**: 无
- **响应示例**:
  ```json
  {
    "message": "用户已成功注销",
    "status": 200
  }
  ```

### 1.5 重置密码
- **请求路径**: `/users/reset_password`
- **请求方法**: POST
- **请求参数**:
  ```json
  {
    "email": "string"  // 注册邮箱
  }
  ```
- **响应示例**:
  ```json
  {
    "message": "重置密码的链接已发送至您的邮箱。",
    "status": 200
  }
  ```

## 2. 错误响应
所有API可能返回的错误格式如下：

```json
{
  "message": "错误信息描述",
  "status": 400/401/403/404/500
}
```

常见状态码：
- 200: 请求成功
- 201: 创建成功
- 400: 请求参数错误
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器内部错误

## 3. 认证说明
- 除注册和登录外，所有API都需要用户登录后才能访问
- 登录后会创建session，后续请求会自动携带session信息
- session过期需要重新登录

## 4. 使用建议
1. 所有请求都应该处理可能的错误响应
2. 密码传输前建议进行加密
3. 请求时注意添加适当的错误处理机制

## 5. 待实现的API
1. 食谱管理API
   - 创建食谱
   - 修改食谱
   - 删除食谱
   - 查询食谱

2. 食材管理API
   - 添加食材
   - 更新食材
   - 删除食材
   - 查询食材

3. 卡路里追踪API
   - 记录摄入
   - 查看统计
   - 设置目标
