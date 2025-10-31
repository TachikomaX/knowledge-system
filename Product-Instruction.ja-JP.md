# ナレッジ管理システム（Knowledge Management System, KMS）製品設計書

## 1. 製品背景と目標

情報量の増加に伴い、個人やチームは効率的なノート・知識管理が必要です。本システムは「構造化保存・高速検索・AIによる知識加工」を提供し、ユーザーが以下を実現できることを目指します：

* ノートの記録と分類
* 知識の高速検索
* AIによる自動要約・分類・Q&A

---

## 2. コア機能

### 2.1 基本機能

1. ユーザー管理
   * 登録・ログイン（JWT）
   * ユーザー情報編集
   * 権限管理（ノートは本人のみ閲覧可能）
2. ノート管理
   * ノート作成（タイトル・本文・タグ・添付）
   * ノート編集・削除
   * 一覧表示・ページング・タグ絞り込み
   * 全文検索（PostgreSQL Full Text Search）
3. タグ管理
   * カスタムタグ作成
   * タグとノートの関連付け

---

### 2.2 AI強化機能

1. 自動要約
   * ノート作成時、DeepSeek APIで要約生成
   * 要約は編集・保存可能
2. 自動分類
   * ノート内容から自動タグ推薦（技術・生活・金融など）
   * ユーザーは選択・修正可能
3. セマンティック検索 / Q&A
   * ノートをベクトル化しChromaDBに保存
   * 自然言語質問で関連ノート検索＋LLMによる回答生成

---

## 3. ユーザーストーリー

* ユーザーとしてノートを保存し、素早く見つけたい
* ノート保存後に自動要約が欲しい
* 検索時に自然言語を使いたい
* AIによる自動タグ付けで整理を効率化したい

---

## 4. システム構成（概要）

* フロントエンド：React + Tailwind CSS
* バックエンド：FastAPI（Python）
* データベース：PostgreSQL（構造化）、ChromaDB（ベクトル検索）
* AIサービス：DeepSeek API
* デプロイ：Docker Compose（FastAPI + Postgres + ChromaDB）、AWS Lightsail/Railway

---

## 5. API概要

| モジュール   | メソッド | パス                          | 説明                           |
| ------------ | -------- | ----------------------------- | ------------------------------ |
| ユーザー管理 | POST     | /api/register                 | 登録                           |
| ユーザー管理 | POST     | /api/login                    | JWT取得                        |
| ユーザー管理 | GET      | /api/user/profile             | ユーザー情報取得               |
| ユーザー管理 | PUT      | /api/user/profile             | ユーザー情報編集               |
| ノート管理   | POST     | /api/notes                    | ノート作成（AI要約・タグ生成） |
| ノート管理   | GET      | /api/notes                    | ノート一覧（ページ・タグ絞込） |
| ノート管理   | GET      | /api/notes/{id}               | ノート詳細                     |
| ノート管理   | PUT      | /api/notes/{id}               | ノート編集                     |
| ノート管理   | DELETE   | /api/notes/{id}               | ノート削除                     |
| ノート管理   | POST     | /api/notes/{id}/favorite      | ノートお気に入り登録/解除      |
| 検索         | GET      | /api/search                   | 全文検索                       |
| タグ管理     | POST     | /api/tags                     | タグ作成                       |
| タグ管理     | GET      | /api/tags                     | タグ一覧取得                   |
| タグ管理     | POST     | /api/notes/{id}/tags          | ノートにタグ追加               |
| タグ管理     | DELETE   | /api/notes/{id}/tags/{tag_id} | ノートからタグ削除             |
| AI強化       | POST     | /api/notes/{id}/summary       | ノート要約生成/編集            |

---

### APIリクエスト/レスポンス例

#### 1. 登録

POST /api/register
リクエスト: { "username": "string", "email": "string", "password": "string" }
レスポンス: { "id": 1, "username": "string", "email": "string" }

#### 2. ログイン

POST /api/login
リクエスト: { "username": "string", "password": "string" }
レスポンス: { "access_token": "jwt_token", "token_type": "bearer" }

#### 3. ノート作成

POST /api/notes
リクエスト: { "title": "string", "content": "string", "tags": ["tag1", "tag2"] }
レスポンス: { "id": 1, "title": "string", "content": "string", "summary": "AI要約", "tags": ["tag1", "tag2"] }

#### 4. セマンティック検索/Q&A

GET /api/semantic-search?query=xxx
レスポンス: { "related_notes": [ { "id": 1, "title": "...", "summary": "..." } ], "answer": "LLM生成回答" }

#### 5. エラー応答

{ "detail": "エラーメッセージ" }

---

### 主なパラメータ

* ページング: ?page=1&page_size=10
* タグ絞込: ?tags=tag1,tag2
* 検索: ?query=キーワード

---

### 権限・セキュリティ

* ノートは本人のみ閲覧可能、JWT認証必須
* 重要操作はトークン検証

---

### AI関連API

* 要約・分類・セマンティック検索はAIサービス（DeepSeek API, ChromaDB）を利用
* AI生成内容は編集可能

---

### 拡張API例

* /api/notes/{id}/comments  コメント・AI対話
* /api/notes/{id}/history   ノート履歴
* /api/files/upload         ファイルアップロード・テキスト抽出
