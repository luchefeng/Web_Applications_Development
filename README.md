# 食有道 - 智能饮食管理系统

## 项目简介
食有道是一个集食材管理、卡路里追踪、菜谱推荐于一体的现代化饮食管理平台。该系统提供两个版本：卡路里管理版和美食探索版，满足不同用户的需求。

## 技术栈
### 前端 (front_vue)
- Vue 3
- Vite
- Vuex
- Vue Router
- Ant Design Vue
- Axios

### 后端 (backend)
- Flask
- SQLAlchemy
- Flask-Login
- Flask-CORSS
- MySQL

## 核心功能
1. 用户系统
   - 注册/登录
   - 版本选择（卡路里管理/美食探索）
   - 个人资料管理

2. 卡路里管理版
   - 卡路里摄入追踪
   - 食材营养成分分析
   - 个性化饮食建议
   - 食材管理

3. 美食探索版
   - 食材库存管理
   - 智能菜谱推荐
   - 菜谱浏览与搜索

## 项目结构

# 项目阿里云部署指南

## 前置条件

1. 已创建一个阿里云ECS实例（建议2核4G或更高配置）
2. 已安装Docker和Docker Compose
3. 已设置域名解析（可选，用于HTTPS）

## 部署步骤

### 1. 准备工作

登录到阿里云服务器：

```bash
ssh root@your_server_ip
```

安装Docker和Docker Compose：

```bash
# 安装Docker
curl -fsSL https://get.docker.com | bash -s docker

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. 上传项目文件

使用scp或其他方式上传项目文件到服务器：

```bash
scp -r ./Web_Applications_Development root@your_server_ip:/root/
```

### 3. 配置环境变量

根据需要修改`production.env`文件：

```bash
cd /root/Web_Applications_Development
nano production.env
```

### 4. 启动项目

运行部署脚本：

```bash
chmod +x deploy.sh
./deploy.sh
```

### 5. 配置HTTPS（可选）

如果需要HTTPS，可以使用Certbot获取Let's Encrypt证书：

```bash
docker run -it --rm --name certbot \
  -v "$(pwd)/certbot/conf:/etc/letsencrypt" \
  -v "$(pwd)/certbot/www:/var/www/certbot" \
  certbot/certbot certonly --webroot \
  --webroot-path=/var/www/certbot \
  --agree-tos --no-eff-email \
  -d your-domain.com -m your-email@example.com
```

获取证书后，取消nginx.conf中HTTPS服务器配置的注释，并替换域名。

### 6. 检查部署状态

```bash
docker-compose ps
```

## 故障排除

1. 如果数据库连接失败，检查`DATABASE_URL`和MySQL配置
2. 查看日志：`docker-compose logs flask-app`
3. 访问测试：`curl http://localhost`
