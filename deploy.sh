#!/bin/bash

# 停止并移除旧的容器
docker-compose down

# 构建新的镜像
docker-compose build

# 使用环境变量文件启动所有服务
docker-compose --env-file production.env up -d

# 数据库迁移（如需要）
docker-compose exec flask-app flask db upgrade

echo "部署完成！"
