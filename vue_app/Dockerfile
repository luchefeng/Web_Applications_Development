FROM node:16

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

# 使用 serve 提供静态文件
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "8080"]
