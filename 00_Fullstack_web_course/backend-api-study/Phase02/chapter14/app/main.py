import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.member_router import router as member_router

# backend-api-study 폴더의 .env 파일을 읽어서 환경변수로 등록한다.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# FastAPI 애플리케이션을 생성한다.
app = FastAPI(
    title="Chapter 14 CORS Frontend Integration",
)

# 허용할 Frontend Origin 목록을 .env의 CORS_ORIGINS에서 읽는다.
# 쉼표(,)로 구분된 문자열을 목록으로 바꾼다.
# 값이 없으면 빈 목록이 되어 아무도 허용하지 않는다.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 회원 Router를 애플리케이션에 등록한다.
# 이제 /members로 시작하는 URL 요청을 처리할 수 있다.
app.include_router(member_router)