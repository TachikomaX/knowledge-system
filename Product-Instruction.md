# 知识管理系统（Knowledge Management System, KMS）产品设计说明书

[🇯🇵 日本語版はこちら](./Product-Instruction.ja-JP.md)  |  [🇬🇧 English version here](./Product-Instruction.en-US.md)

## **1. 产品背景与目标**

随着信息量的增长，个人和团队都需要高效管理自己的笔记、文档和知识。
本系统的目标是提供一个**可结构化存储、快速检索、智能加工**的知识管理平台，帮助用户：

* 记录和分类笔记
* 快速搜索知识
* 利用 AI 自动摘要、分类、问答

---

## **2. 核心功能**

分为 **基础功能**（无 AI）和 **智能功能**（AI 驱动）两部分。

### 2.1 基础功能

1. **用户管理**

   * 注册、登录（JWT）
   * 用户信息修改
   * 权限控制（笔记只对本人可见）

2. **笔记管理**

   * 创建笔记（标题、正文、标签、附件）
   * 编辑笔记
   * 删除笔记
   * 列表分页、按标签筛选
   * 全文搜索（PostgreSQL Full Text Search）

3. **标签管理**

   * 自定义标签
   * 标签关联笔记

---

### 2.2 智能功能（AI增强）

1. **自动摘要**

   * 用户创建笔记后，系统调用 DeepSeek API 生成简短摘要。
   * 摘要可编辑保存。

2. **自动分类**

   * 系统根据笔记内容，自动推荐标签（如技术、生活、金融）。
   * 用户可选择接受或修改。

3. **语义搜索 / 知识问答**

   * 将笔记向量化存储到向量数据库（ChromaDB）
   * 用户输入自然语言问题，系统检索相关笔记，并用 LLM 生成答案。

---

## **3. 用户故事（User Story）**

* 作为一个用户，我希望能够保存笔记，并能快速找到它们。
* 作为一个用户，我希望笔记保存后自动生成摘要，方便我快速回顾。
* 作为一个用户，我希望搜索时可以用自然语言，而不是只匹配关键词。
* 作为一个用户，我希望 AI 能帮我自动打标签，让我更快整理知识。

---

## **4. 系统架构设计（概要）**

* **前端**（可选）：React + Tailwind CSS
* **后端**：FastAPI（Python）
* **数据库**：PostgreSQL（结构化数据）、ChromaDB（向量搜索）
* **AI服务**：DeepSeek API
* **部署**：Docker Compose（FastAPI + Postgres + ChromaDB），后续部署到 AWS Lightsail / Railway

---

## **5. API 概要**

| 模块     | 方法   | 路径                          | 描述                            |
| -------- | ------ | ----------------------------- | ------------------------------- |
| 用户管理 | POST   | /api/register                 | 注册                            |
| 用户管理 | POST   | /api/login                    | 登录获取JWT                     |
| 用户管理 | GET    | /api/user/profile             | 获取当前用户信息                |
| 用户管理 | PUT    | /api/user/profile             | 修改用户信息                    |
| 笔记管理 | POST   | /api/notes                    | 创建笔记（调用AI生成摘要&标签） |
| 笔记管理 | GET    | /api/notes                    | 获取笔记列表（分页、标签筛选）  |
| 笔记管理 | GET    | /api/notes/{id}               | 查看单条笔记                    |
| 笔记管理 | PUT    | /api/notes/{id}               | 编辑笔记                        |
| 笔记管理 | DELETE | /api/notes/{id}               | 删除笔记                        |
| 笔记管理 | POST   | /api/notes/{id}/favorite      | 收藏/取消收藏笔记               |
| 搜索     | GET    | /api/search                   | 全文搜索                        |
| 标签管理 | POST   | /api/tags                     | 创建标签                        |
| 标签管理 | GET    | /api/tags                     | 获取标签列表                    |
| 标签管理 | POST   | /api/notes/{id}/tags          | 给笔记添加标签                  |
| 标签管理 | DELETE | /api/notes/{id}/tags/{tag_id} | 移除笔记标签                    |
| AI增强   | POST   | /api/notes/{id}/summary       | 生成/编辑笔记摘要               |

---

### API 请求/响应示例

#### 1. 注册

POST /api/register
请求: { "username": "string", "email": "string", "password": "string" }
响应: { "id": 1, "username": "string", "email": "string" }

#### 2. 登录

POST /api/login
请求: { "username": "string", "password": "string" }
响应: { "access_token": "jwt_token", "token_type": "bearer" }

#### 3. 创建笔记

POST /api/notes
请求: { "title": "string", "content": "string", "tags": ["tag1", "tag2"] }
响应: { "id": 1, "title": "string", "content": "string", "summary": "AI生成摘要", "tags": ["tag1", "tag2"] }

#### 4. 语义搜索/知识问答

GET /api/semantic-search?query=xxx
响应: { "related_notes": [ { "id": 1, "title": "...", "summary": "..." } ], "answer": "LLM生成答案" }

#### 5. 错误响应

{ "detail": "错误信息" }

---

### 主要参数说明

* 分页参数: ?page=1&page_size=10
* 标签筛选: ?tags=tag1,tag2
* 搜索参数: ?query=关键词

---

### 权限与安全

* 所有笔记仅对本人可见，需JWT鉴权。
* 敏感操作需token验证。

---

### AI相关接口说明

* 自动摘要、自动分类、语义搜索均调用后端AI服务（DeepSeek API、ChromaDB）。
* 支持编辑AI生成内容。

---

### 扩展接口建议

* /api/notes/{id}/comments  评论与AI对话
* /api/notes/{id}/history   笔记版本历史
* /api/files/upload         文件上传与文本提取

---

## **6. 数据库表（核心字段）**

### users

* id (PK)
* username
* password\_hash
* email
* created\_at

### notes

* id (PK)
* user\_id (FK → users.id)
* title
* content
* summary
* created\_at
* updated\_at

### tags

* id (PK)
* name

### note\_tags

* note\_id (FK → notes.id)
* tag\_id (FK → tags.id)

---

## **7. AI 功能调用流程（例：自动摘要）**

1. 用户通过 `/api/notes` 创建笔记
2. FastAPI 保存原始笔记到数据库
3. 后端调用 DeepSeek API → 获取笔记摘要
4. 更新笔记记录，返回给前端

---

## **8. 可扩展功能**

* AI对谈，在评论区与AI针对某条记录进行讨论
* 多用户共享知识（团队版）
* 笔记版本历史
* 支持上传文件并自动提取文本
* 接入 OCR（识别图片中的文字）
