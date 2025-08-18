# Knowledge Management System

一个基于 **FastAPI + PostgreSQL + React** 的知识管理系统，支持笔记记录、标签管理、AI 自动摘要 & 语义搜索（集成 DeepSeek API）。

---

## 🚀 功能特性

- 用户注册 / 登录 / JWT 认证
- 笔记 CRUD
- 标签管理
- 全文搜索 & AI 语义搜索
- AI 自动摘要 & 标签生成（DeepSeek API）
- 前后端分离，基于 Docker Compose 一键启动

---

## 📦 本地开发环境

### 1. 克隆仓库

```bash
git clone https://github.com/yourname/knowledge-system.git
cd knowledge-system
````

### 2. 复制环境变量文件

```bash
cp .env.example .env
```

修改 `.env` 中的配置，例如：

```env
POSTGRES_USER=kms_user
POSTGRES_PASSWORD=kms_pass
POSTGRES_DB=kms_db
DEEPSEEK_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

### 3. 启动服务

```bash
docker-compose up -d
```

服务启动后：

- 后端 API: [http://localhost:8000](http://localhost:8000)
- 前端: [http://localhost:3000](http://localhost:3000)
- 数据库: localhost:5432 (用户名/密码见 `.env`)

### 4. 初始化数据库

进入后端容器：

```bash
docker exec -it kms_backend bash
```

运行 Alembic 迁移：

```bash
alembic upgrade head
```

### 5. 测试 API

启动成功后，可以访问：

- Swagger API 文档: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc 文档: [http://localhost:8000/redoc](http://localhost:8000/redoc)

示例（创建用户）：

```bash
curl -X POST http://localhost:8000/api/register \
    -H "Content-Type: application/json" \
    -d '{"username": "test", "email": "test@example.com", "password": "123456"}'
```

---

## 🧑‍💻 开发模式

### 目录结构说明

```markdown
knowledge-system/
├── backend/                  # Python FastAPI 后端
│   ├── app/
│   │   ├── api/              # 路由层（用户、笔记、搜索等）
│   │   ├── core/             # 配置（JWT、DB连接、日志）
│   │   ├── models/           # SQLAlchemy 模型
│   │   ├── schemas/          # Pydantic 数据校验
│   │   ├── services/         # 业务逻辑（AI调用、搜索等）
│   │   ├── db.py             # 数据库初始化
│   │   └── main.py           # FastAPI 入口
│   ├── alembic/              # 数据库迁移
│   ├── tests/                # 单元测试
│   ├── requirements.txt      # Python依赖
│   └── Dockerfile
│
├── frontend/                 # React 前端
│   ├── src/
│   │   ├── components/       # 组件
│   │   ├── pages/            # 页面（登录、笔记列表、编辑器）
│   │   ├── services/         # 调用后端 API 的封装
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml        # 本地开发环境编排
├── .env.example              # 环境变量模板
├── README.md                 # 项目说明
└── LICENSE                   # 开源协议

```

### 后端

进入 `backend/`：

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 前端

进入 `frontend/`：

```bash
npm install
npm run dev
```

---

## 📜 License

MIT

---

只需要：  

1. `git clone`  
2. `cp .env.example .env`  
3. `docker-compose up -d`  
4. `alembic upgrade head`  
就能跑起来前后端和数据库了 ✅  
