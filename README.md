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
```

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

### 后端

#### 🚀 后端功能概览

#### 📂 后端目录结构

#### ⚙️ 环境准备

#### 🧪 调试流程

进入 `backend/`：

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

进入本地docker启动的db

```bash
docker exec -it kms_postgres psql -U kms_user -d kms_db
```

### 前端

基于 **React + Vite + TailwindCSS** 的前端实现，提供用户登录、笔记管理、标签筛选、全文搜索与语义搜索等功能，后端 API 参考 [API 概要](#-api-概要)。

---

#### 🚀 前端功能概览

- 用户注册与登录（JWT 认证）
- 笔记管理（增删改查、自动生成摘要与标签）
- 标签管理与筛选
- 全文搜索
- 语义搜索（调用向量搜索 API）

---

#### 📂 前端目录结构

```txt
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/                # API 封装
│   │   └── client.ts       # Axios 实例，处理JWT
│   ├── components/         # 公共组件
│   │   ├── Navbar.tsx
│   │   └── ProtectedRoute.tsx
│   ├── pages/              # 页面模块
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Notes.tsx
│   │   ├── NoteDetail.tsx
│   │   ├── Search.tsx
│   │   └── SemanticSearch.tsx
│   ├── hooks/              # 自定义 hooks
│   │   └── useAuth.ts
│   ├── App.tsx             # 路由配置
│   ├── main.tsx            # 应用入口
│   └── index.css           # Tailwind 样式入口
├── .env                    # 环境变量（API_BASE_URL）
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

#### ⚙️ 环境准备

##### 1. 安装依赖

```bash
cd frontend
npm install
```

主要依赖：

- React 18
- React Router DOM
- Axios
- TailwindCSS
- shadcn/ui（UI 组件库，可选）

##### 2. 配置环境变量

在 `frontend/.env` 中设置后端 API 地址，例如：

```code
VITE_API_BASE_URL=http://localhost:8000
```

##### 3. 启动开发服务器

```bash
npm run dev
```

默认运行在 [http://localhost:5173](http://localhost:5173)

##### 4. 打包生产环境

```bash
npm run build
```

打包结果在 `dist/` 目录，可用 Nginx 或 Vercel 部署。

---

#### 🔑 认证机制说明

- 登录后，后端返回 **JWT Token**。
- 前端保存 token（推荐存在 `localStorage`）。
- Axios 请求时自动在 Header 添加：
  
```code
Authorization: Bearer <token>
```

- 退出登录时清理 token。

---

#### 🧪 调试流程

1. **启动后端**
   确保 FastAPI 后端（含 `/api/*` 接口）已运行并监听 8000 端口。

2. **启动前端**

   ```bash
   npm run dev
   ```

3. **调试用户流程**

   - 打开 [http://localhost:5173](http://localhost:5173)
   - 注册 → 登录 → 跳转笔记页
   - 创建笔记 → 自动生成摘要和标签 → 列表展示
   - 进入搜索页面调试全文搜索/语义搜索接口

4. **接口调试**

   - 在 `src/api/client.ts` 里可打开 `console.log` 调试请求。
   - 使用 `curl` 或 `Postman` 验证后端接口是否可用。

#### 📌 API 概要

| 模块     | 方法   | 路径                 | 描述                            |
| -------- | ------ | -------------------- | ------------------------------- |
| 用户管理 | POST   | /api/register        | 注册                            |
| 用户管理 | POST   | /api/login           | 登录获取JWT                     |
| 笔记管理 | POST   | /api/notes           | 创建笔记（调用AI生成摘要&标签） |
| 笔记管理 | GET    | /api/notes           | 获取笔记列表（分页、标签筛选）  |
| 笔记管理 | GET    | /api/notes/{id}      | 查看单条笔记                    |
| 笔记管理 | PUT    | /api/notes/{id}      | 编辑笔记                        |
| 笔记管理 | DELETE | /api/notes/{id}      | 删除笔记                        |
| 搜索     | GET    | /api/search          | 全文搜索                        |
| 语义搜索 | POST   | /api/semantic-search | 向量搜索并生成答案              |

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
