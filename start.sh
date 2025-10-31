#!/bin/bash
# 启动后端服务
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
# 启动nginx
nginx -g 'daemon off;'
