
import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


# 1. 기존 backend-api-study/.env 로드
load_dotenv()


# 2. Database 연결 정보
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)


# 3. Engine 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "options": f"-c search_path={os.getenv('DB_SCHEMA', 'public')}"
    },
)


# 4. Session 생성기
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# 5. ORM Model의 공통 부모 클래스
class Base(DeclarativeBase):
    pass



class Base(DeclarativeBase):
    pass


# 요청마다 새로운 DB Session을 만든다.
def get_db():
    db = SessionLocal()

    try:
        # Router가 DB Session을 사용할 수 있도록 전달한다.
        yield db

    finally:
        # 요청 처리가 성공하거나 실패해도
        # 마지막에는 반드시 DB Session을 닫는다.
        db.close()