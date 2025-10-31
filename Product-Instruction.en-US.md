# Knowledge Management System (KMS) Product Design Document

## 1. Product Background & Goals

With the growth of information, individuals and teams need efficient ways to manage notes, documents, and knowledge. This system aims to provide a platform for **structured storage, fast retrieval, and intelligent processing** to help users:

* Record and categorize notes
* Quickly search knowledge
* Use AI for automatic summarization, classification, and Q&A

---

## 2. Core Features

### 2.1 Basic Features

1. User Management
   * Registration & Login (JWT)
   * Edit user information
   * Permission control (notes are private to the owner)
2. Note Management
   * Create notes (title, content, tags, attachments)
   * Edit and delete notes
   * List with pagination, filter by tags
   * Full-text search (PostgreSQL Full Text Search)
3. Tag Management
   * Custom tags
   * Associate tags with notes

---

### 2.2 Intelligent Features (AI Enhanced)

1. Auto Summarization
   * After note creation, system calls DeepSeek API to generate a summary
   * Summary can be edited and saved
2. Auto Classification
   * System recommends tags based on note content (e.g., tech, life, finance)
   * User can accept or modify
3. Semantic Search / Knowledge Q&A
   * Notes are vectorized and stored in ChromaDB
   * User asks questions in natural language, system retrieves relevant notes and generates answers using LLM

---

## 3. User Stories

* As a user, I want to save notes and find them quickly
* As a user, I want notes to be automatically summarized for quick review
* As a user, I want to search using natural language, not just keywords
* As a user, I want AI to auto-tag my notes for easier organization

---

## 4. System Architecture (Overview)

* Frontend: React + Tailwind CSS
* Backend: FastAPI (Python)
* Database: PostgreSQL (structured), ChromaDB (vector search)
* AI Service: DeepSeek API
* Deployment: Docker Compose (FastAPI + Postgres + ChromaDB), AWS Lightsail / Railway

---

## 5. API Overview

| Module | Method | Path                          | Description                       |
| ------ | ------ | ----------------------------- | --------------------------------- |
| User   | POST   | /api/register                 | Register                          |
| User   | POST   | /api/login                    | Get JWT                           |
| User   | GET    | /api/user/profile             | Get current user info             |
| User   | PUT    | /api/user/profile             | Edit user info                    |
| Note   | POST   | /api/notes                    | Create note (AI summary & tags)   |
| Note   | GET    | /api/notes                    | Get notes list (pagination, tags) |
| Note   | GET    | /api/notes/{id}               | Get single note                   |
| Note   | PUT    | /api/notes/{id}               | Edit note                         |
| Note   | DELETE | /api/notes/{id}               | Delete note                       |
| Note   | POST   | /api/notes/{id}/favorite      | Favorite/unfavorite note          |
| Search | GET    | /api/search                   | Full-text search                  |
| Tag    | POST   | /api/tags                     | Create tag                        |
| Tag    | GET    | /api/tags                     | Get tag list                      |
| Tag    | POST   | /api/notes/{id}/tags          | Add tag to note                   |
| Tag    | DELETE | /api/notes/{id}/tags/{tag_id} | Remove tag from note              |
| AI     | POST   | /api/notes/{id}/summary       | Generate/edit note summary        |

---

### API Request/Response Examples

#### 1. Register

POST /api/register
Request: { "username": "string", "email": "string", "password": "string" }
Response: { "id": 1, "username": "string", "email": "string" }

#### 2. Login

POST /api/login
Request: { "username": "string", "password": "string" }
Response: { "access_token": "jwt_token", "token_type": "bearer" }

#### 3. Create Note

POST /api/notes
Request: { "title": "string", "content": "string", "tags": ["tag1", "tag2"] }
Response: { "id": 1, "title": "string", "content": "string", "summary": "AI generated summary", "tags": ["tag1", "tag2"] }

#### 4. Semantic Search / Q&A

GET /api/semantic-search?query=xxx
Response: { "related_notes": [ { "id": 1, "title": "...", "summary": "..." } ], "answer": "LLM generated answer" }

#### 5. Error Response

{ "detail": "Error message" }

---

### Main Parameters

* Pagination: ?page=1&page_size=10
* Tag filter: ?tags=tag1,tag2
* Search: ?query=keyword

---

### Permissions & Security

* All notes are private to the owner, JWT authentication required
* Sensitive operations require token verification

---

### AI Related APIs

* Auto summary, classification, and semantic search use backend AI services (DeepSeek API, ChromaDB)
* AI generated content can be edited

---

### Suggested Extension APIs

* /api/notes/{id}/comments  Comments & AI chat
* /api/notes/{id}/history   Note version history
* /api/files/upload         File upload & text extraction
