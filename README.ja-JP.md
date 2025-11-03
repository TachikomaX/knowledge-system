# ナレッジ管理システム

**FastAPI + PostgreSQL + React** をベースにしたナレッジ管理システムです。ノート記録、タグ管理、AI自動要約＆セマンティック検索（DeepSeek API連携）をサポートします。

![ログイン画面プレビュー](./frontend/public/login-preview.png)

![ホーム画面プレビュー](./frontend/public/note-preview.png)

---

## 技術スタック

- FastAPI
- PostgreSQL
- React + Vite
- TailwindCSS
- Docker Compose
- DeepSeek API

---

## 必要環境

- Docker & Docker Compose
- Python >= 3.9
- Node.js >= 18

---

## クイックスタート

1. リポジトリをクローン

   ```bash
   git clone https://github.com/yourname/knowledge-system.git
   cd knowledge-system
   ```

2. 環境変数ファイルをコピー

   ```bash
   cp .env.example .env
   ```

   `.env` を編集します（例）：

   ```env
   POSTGRES_USER=kms_user
   POSTGRES_PASSWORD=kms_pass
   POSTGRES_DB=kms_db
   DEEPSEEK_API_KEY=your_api_key_here
   SECRET_KEY=your_secret_key_here
   ```

3. サービスを起動

   ```bash
   docker-compose up -d
   ```

   起動後：
   - バックエンドAPI: [http://localhost:8000](http://localhost:8000)
   - フロントエンド: [http://localhost:3000](http://localhost:3000)
   - データベース: localhost:5432（認証情報は `.env` 参照）
4. データベース初期化

   ```bash
   docker exec -it kms_backend bash
   alembic upgrade head
   ```

---

## 主な機能

- ユーザー登録 / ログイン / JWT認証
- ノートCRUD
- タグ管理
- 全文検索＆セマンティック検索
- AI自動要約＆タグ生成（DeepSeek API）
- フロント・バックエンド分離、Docker Composeで一括起動

---

## ディレクトリ構成

### バックエンド

```txt
backend/
├── alembic/              # データベースマイグレーションスクリプト
│   ├── versions/         # マイグレーション履歴
│   └── env.py            # Alembic環境設定
├── app/
│   ├── api/              # ルート（ユーザー、ノート、タグ等）
│   ├── auth/             # 認証関連ロジック
│   ├── crud/             # DB操作
│   ├── models/           # ORMモデル
│   ├── schemas/          # Pydanticバリデーションモデル
│   ├── utils/            # ユーティリティ（AI要約等）
│   ├── config.py         # 設定ファイル
│   ├── db.py             # DB接続
│   └── main.py           # FastAPIアプリエントリ
├── tests/                # バックエンドテスト
├── pyproject.toml        # 依存・設定
├── alembic.ini           # Alembic設定
└── README.md             # バックエンド説明
```

### フロントエンド

```txt
frontend/
├── public/                # 静的アセット（画像、SVG等）
├── src/
│   ├── api/               # APIラッパー（Axios、APIメソッド）
│   ├── components/        # 共通コンポーネント（カード、ダイアログ、サイドバー等）
│   ├── pages/             # ページモジュール（ログイン、登録、ノート、タグ等）
│   ├── assets/            # 画像、SVG
│   ├── hooks/             # カスタムフック
│   ├── App.tsx            # ルーティング設定
│   ├── main.tsx           # アプリエントリ
│   └── index.css          # Tailwindスタイル
├── package.json           # 依存
├── tsconfig.json          # TypeScript設定
├── vite.config.ts         # Vite設定
└── README.md              # フロントエンド説明
```

---

## APIドキュメント

- [Swagger UI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

---

## コントリビューション

歓迎します！

1. リポジトリをFork
2. 新しいブランチ作成（例：`feature/xxx`）
3. PRを提出し、変更内容を記載
4. CIチェックを通過すること

提案・質問はIssueまたはDiscussionsへ。

---

## 問い合わせ

- IssueまたはDiscussions
- `alvingcy1121@gmail.com`

---

## ライセンス

MIT © 2025 HyperionXX

---

## AWS EC2 へのデプロイ（CI/CD 連携）

本リポジトリには、プロダクション向けの簡易フロー（CIでイメージ作成、CDでEC2へデプロイ）を用意しています。

1. GitHub リポジトリの Secrets を設定（Settings → Secrets and variables → Actions）
   - EC2_HOST：EC2 のパブリックIP/ドメイン
   - EC2_USER：EC2 ログインユーザー（例：ubuntu / ec2-user）
   - EC2_SSH_KEY：上記ユーザーの秘密鍵（PEM）
   - GHCR_USERNAME：GitHub ユーザー名
   - GHCR_TOKEN：GitHub PAT（read:packages）。EC2 側で GHCR ログインに使用

2. EC2 初期化（Docker/Compose の導入、/opt/kms と .env の準備）

   ```bash
   curl -fsSL https://raw.githubusercontent.com/TachikomaX/knowledge-system/master/scripts/ec2-init.sh | bash
   ```

   - スクリプトは /opt/kms を作成し、/opt/kms/.env のテンプレートを生成します。以下を記入してください：
     - DATABASE_URL=postgresql+psycopg2://\<user\>:\<password\>@\<rds-endpoint\>:5432/\<db\>
     - DEEPSEEK_API_KEY=your_api_key
     - VITE_API_URL=/api

3. デプロイのトリガー
   - master/main への push で、イメージのビルド＆プッシュ（.github/workflows/docker.yml）と EC2 へのデプロイ（.github/workflows/deploy-ec2.yml）が実行されます
   - もしくは Actions から Deploy to EC2 ワークフローを手動実行

4. アクセス
   - アプリは 80 番ポートで提供（コンテナ内の Nginx は 3000、ホストで 80:3000 マッピング）
   - HTTPS が必要な場合、Nginx または ALB で証明書を設定してください
