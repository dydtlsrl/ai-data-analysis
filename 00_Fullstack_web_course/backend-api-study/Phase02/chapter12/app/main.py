from fastapi import FastAPI

from app.routers.member_router import router as member_router


# FastAPI 애플리케이션을 생성한다.
app = FastAPI(
    title="Chapter 12 ORM Member CRUD",
)


# 회원 Router를 애플리케이션에 등록한다.
# 이제 /members로 시작하는 URL 요청을 처리할 수 있다.
app.include_router(member_router)