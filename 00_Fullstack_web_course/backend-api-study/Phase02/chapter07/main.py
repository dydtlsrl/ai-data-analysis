
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

from common.db import get_connection


# ==================================
# 1. Pydantic Models
# ==================================

# 회원 등록 시 입력받을 데이터
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


# 회원 등록 후 반환할 데이터
class MemberResponse(MemberCreate):
    member_id: int


# 회원 전체 수정 시 입력받을 데이터
class MemberUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


# ==================================
# 2. Database Functions
# ==================================

# 중복 이메일 확인 함수
def check_duplicate_email(email: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT member_id
                FROM members
                WHERE email = %s;
                """,
                (email,),
            )
            return cursor.fetchone()


# 중복 이메일 검증 함수
def validate_duplicate_email(email: str):
    existing = check_duplicate_email(email)

    if existing:
        raise HTTPException(
            status_code=409,
            detail="이미 등록된 이메일입니다.",
        )


# 회원 등록 함수
def insert_member(member: MemberCreate):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING member_id, name, email, age;
                """,
                (member.name, str(member.email), member.age),
            )
            return cursor.fetchone()


# 회원 한 명 조회 함수
def fetch_member_by_id(member_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT member_id, name, email, age
                FROM members
                WHERE member_id = %s;
                """,
                (member_id,),
            )
            return cursor.fetchone()


# ==================================
# 3. FastAPI Application
# ==================================

app = FastAPI(
    title="Chapter 08 - Member API",
    description="회원 등록, 조회 및 전체 수정 실습",
    version="1.0.0",
)


# ==================================
# 4. API Endpoints
# ==================================

# 기본 페이지
@app.get("/")
def root():
    return {
        "message": "Chapter 08 Member API Server is running"
    }


# 회원 등록 API
@app.post(
    "/members",
    response_model=MemberResponse,
    status_code=201,
)
def create_member(member: MemberCreate):
    validate_duplicate_email(str(member.email))

    return insert_member(member)


# 회원 한 명 조회 API
@app.get(
    "/members/{member_id}",
    response_model=MemberResponse,
)
def get_member(member_id: int):
    member = fetch_member_by_id(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return member


# ==================================
# 5. PUT - 회원 전체 수정 API
# ==================================

@app.put(
    "/members/{member_id}",
    response_model=MemberResponse,
)
def update_member(member_id: int, member: MemberUpdate):

    with get_connection() as conn:
        with conn.cursor() as cursor:

            # 1. 수정할 회원이 존재하는지 확인
            cursor.execute(
                """
                SELECT member_id
                FROM members
                WHERE member_id = %s;
                """,
                (member_id,),
            )

            if cursor.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Member not found",
                )

            # 2. 다른 회원과 이메일 중복 확인
            cursor.execute(
                """
                SELECT member_id
                FROM members
                WHERE email = %s
                AND member_id <> %s;
                """,
                (str(member.email), member_id),
            )

            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=409,
                    detail="이미 등록된 이메일입니다.",
                )

            # 3. 회원 전체 수정
            cursor.execute(
                """
                UPDATE members
                SET name = %s,
                    email = %s,
                    age = %s
                WHERE member_id = %s
                RETURNING member_id, name, email, age;
                """,
                (
                    member.name,
                    str(member.email),
                    member.age,
                    member_id,
                ),
            )

            # 4. 수정 결과 가져오기
            updated = cursor.fetchone()

            # 5. 트랜잭션 확정
            conn.commit()

            return updated
