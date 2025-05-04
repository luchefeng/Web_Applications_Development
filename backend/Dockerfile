FROM python:3.9-slim-bullseye

# 创建非root用户
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# 安装依赖前更新包管理器
RUN apt-get update && apt-get install -y --no-install-recommends gcc libffi-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 修改文件夹权限
RUN chown -R appuser:appuser /app
RUN mkdir -p /app/flask_session_cache && chown -R appuser:appuser /app/flask_session_cache

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 5000

# 使用gunicorn作为生产环境Web服务器
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app2:app"]
