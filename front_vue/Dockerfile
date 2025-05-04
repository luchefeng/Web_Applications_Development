# 构建阶段
FROM node:16-alpine as build-stage

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# 设置API URL为后端容器服务名
ENV VITE_API_BASE_URL=/api

RUN npm run build

# 生产阶段
FROM nginx:stable-alpine as production-stage

# 添加自定义nginx配置，解决单页应用路由问题
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 删除默认的nginx静态资源
RUN rm -rf /usr/share/nginx/html/*

# 从构建阶段拷贝构建结果到nginx容器
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 创建非root用户
RUN adduser -D -H -u 1001 -s /sbin/nologin nginx-user && \
    chown -R nginx-user:nginx-user /usr/share/nginx/html

# 使用非root用户运行
USER nginx-user

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
