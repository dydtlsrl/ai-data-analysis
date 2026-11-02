
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row


# 프로젝트 루트 경로
BASE_DIR = Path(__file__).resolve().parent.parent

# 공통 .env 파일 불러오기
load_dotenv(BASE_DIR / ".env")


# PostgreSQL 공통 연결 함수
def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        options=f"-c search_path={os.getenv('DB_SCHEMA', 'public')}",
        row_factory=dict_row,
    )
