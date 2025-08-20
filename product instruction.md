# 知识管理系统（Knowledge Management System, KMS）产品设计说明书

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
3. 后端异步调用 DeepSeek API → 获取摘要和推荐标签
4. 更新笔记记录，返回给前端

---

## **8. 可扩展功能**

* AI对谈，在评论区与AI针对某条记录进行讨论
* 多用户共享知识（团队版）
* 笔记版本历史
* 支持上传文件并自动提取文本
* 接入 OCR（识别图片中的文字）

