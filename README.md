# Knowledge Management System

一个基于 **FastAPI + PostgreSQL + React** 的知识管理系统，支持笔记记录、标签管理、AI 自动摘要 & 语义搜索（集成 DeepSeek API）。

![登录界面预览](./frontend/public/login-preview.png)

![首页界面预览](./frontend/public/note-preview.png)

---

## 技术栈

- FastAPI
- PostgreSQL
- React + Vite
- TailwindCSS
- Docker Compose
- DeepSeek API

---

## 环境依赖

- Docker & Docker Compose
- Python >= 3.9
- Node.js >= 18

---

## 快速开始

1. 克隆仓库

   ```bash
   git clone https://github.com/yourname/knowledge-system.git
   cd knowledge-system
   ```

2. 复制环境变量文件

   ```bash
   cp .env.example .env
   ```

   修改 `.env` 配置，例如：

   ```env
   POSTGRES_USER=kms_user
   POSTGRES_PASSWORD=kms_pass
   POSTGRES_DB=kms_db
   DEEPSEEK_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

3. 启动服务

   ```bash
   docker-compose up -d
   ```

   服务启动后：
   - 后端 API: [http://localhost:8000](http://localhost:8000)
   - 前端: [http://localhost:3000](http://localhost:3000)
   - 数据库: localhost:5432 (用户名/密码见 `.env`)
4. 初始化数据库

   ```bash
   docker exec -it kms_backend bash
   alembic upgrade head
   ```

---

## 功能特性

- 用户注册 / 登录 / JWT 认证
- 笔记 CRUD
- 标签管理
- 全文搜索 & AI 语义搜索
- AI 自动摘要 & 标签生成（DeepSeek API）
- 前后端分离，基于 Docker Compose 一键启动

---

## 目录结构

### 后端

```txt
backend/
├── alembic/              # 数据库迁移脚本
│   ├── versions/         # 迁移历史
│   └── env.py            # Alembic 环境配置
├── app/
│   ├── api/              # 路由接口（用户、笔记、标签等）
│   ├── auth/             # 认证相关逻辑
│   ├── crud/             # 数据库操作封装
│   ├── models/           # ORM 数据模型
│   ├── schemas/          # Pydantic 数据校验模型
│   ├── utils/            # 工具类（如 AI 摘要）
│   ├── config.py         # 配置文件
│   ├── db.py             # 数据库连接
│   └── main.py           # FastAPI 应用入口
├── tests/                # 后端测试
├── pyproject.toml        # 后端依赖与配置
├── alembic.ini           # Alembic 配置
└── README.md             # 后端说明文档
```

### 前端

```txt
frontend/
├── public/                # 静态资源（图片、SVG 等）
├── src/
│   ├── api/               # API 封装（Axios 实例、接口方法）
│   ├── components/        # 公共组件（卡片、弹窗、侧边栏等）
│   ├── pages/             # 页面模块（登录、注册、笔记、标签等）
│   ├── assets/            # 前端图片、SVG
│   ├── hooks/             # 自定义 hooks
│   ├── App.tsx            # 路由配置
│   ├── main.tsx           # 应用入口
│   └── index.css          # Tailwind 样式入口
├── package.json           # 前端依赖
├── tsconfig.json          # TypeScript 配置
├── vite.config.ts         # Vite 配置
└── README.md              # 前端说明文档
```

---

## API 文档

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

---

## 贡献指南

欢迎参与贡献！

1. Fork 本仓库
2. 新建分支（如 `feature/xxx`）
3. 提交 PR 并描述变更内容
4. 代码需通过 CI 检查

如有建议或问题，请提交 Issue 或参与 Discussions。

---

## 问题反馈

- 提交 Issue 或参与 Discussions
- `alvingcy1121@gmail.com`

---

## License

MIT © 2025 HyperionXX

---
