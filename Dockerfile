# 前端构建阶段
ARG NODE_IMAGE=node:20
FROM ${NODE_IMAGE} AS frontend-build
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install && npm audit fix --force
COPY frontend/ ./
RUN npm run build

# 后端构建阶段
FROM python:3.10-slim AS backend-build
WORKDIR /backend
COPY backend/pyproject.toml backend/poetry.lock ./
RUN apt-get update && apt-get install -y build-essential curl && \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
COPY backend/ ./

# 生产镜像
FROM python:3.10-slim
WORKDIR /app
# 拷贝后端
COPY --from=backend-build /backend /app/backend
# 拷贝前端静态资源
COPY --from=frontend-build /frontend/dist /app/frontend_dist
# 安装nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
COPY nginx.conf /etc/nginx/nginx.conf
# 启动脚本
COPY start.sh /start.sh
RUN chmod +x /start.sh
EXPOSE 8000 3000
CMD ["/start.sh"]
