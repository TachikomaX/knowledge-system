#!/bin/bash
set -euo pipefail

# 切换到后端目录，确保 Python 模块路径正确
cd /app/backend

# 启动后端服务（使用 python -m 方式更稳健）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 启动 nginx（前端静态和 /api 反代）
nginx -g 'daemon off;'
