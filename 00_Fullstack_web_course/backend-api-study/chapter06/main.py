from fastapi import FastAPI

from routers.members import router as members_router


app = FastAPI(
    title="Chapter 06 - Member API",
    description="FastAPI와 PostgreSQL 연동 실습",
    version="1.0.0",
)


# 회원 API 연결
app.include_router(members_router)


@app.get("/")
def root():
    return {"message": "Member API Server is running"}