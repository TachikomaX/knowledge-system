#!/bin/bash
set -euo pipefail

# 切换到后端目录，确保 Python 模块路径正确
cd /app/backend

# 等待数据库并执行迁移（最多重试 10 次）
attempt=0
until alembic upgrade head; do
	attempt=$((attempt+1))
	if [ "$attempt" -ge 10 ]; then
		echo "[start] Alembic migration failed after $attempt attempts, exiting."
		exit 1
	fi
	echo "[start] Alembic migration failed, retrying in 3s... ($attempt/10)"
	sleep 3
done

# 启动后端服务（使用 python -m 方式更稳健）
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 启动 nginx（前端静态和 /api 反代）
nginx -g 'daemon off;'
