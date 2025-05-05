# Stage 1: Build the frontend
FROM node:18 AS frontend-builder
WORKDIR /app
COPY front_vue/ ./front_vue/
RUN cd front_vue && npm install && npm run build  # 修正npm run build命令

# Stage 2: Build the backend (Flask)
FROM python:3.11-slim
WORKDIR /app

# Copy backend files
COPY backend/ ./backend/

# 修正.env文件的路径 - 使用backend/.env而不是.env
COPY backend/.env ./backend/.env

COPY requirements.txt ./requirements.txt
COPY --from=frontend-builder /app/front_vue/dist ./frontend-dist/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Set default environment variables (can be overridden at runtime)
ENV FLASK_APP=backend/app2.py
ENV FLASK_ENV=production

# Command to run the Flask application
CMD ["python", "backend/app2.py"]
