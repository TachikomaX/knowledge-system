import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1️⃣ 加载环境变量
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")  # 从配置读取

# 2️⃣ 创建 SQLAlchemy 引擎
engine = create_engine(
    DATABASE_URL,
    echo=True,  # True 时打印所有 SQL，调试用
    future=True)

# 3️⃣ 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4️⃣ 声明 Base
Base = declarative_base()


# 5️⃣ 依赖函数（用于 FastAPI 注入 session）
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
