
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, model_validator

from common.db import get_connection


# ==================================
# 1. Pydantic Models
# ==================================

# 회원 등록 시 입력받을 데이터
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


# 회원 전체 수정 시 입력받을 데이터 (PUT)
class MemberUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


# 회원 부분 수정 시 입력받을 데이터 (PATCH)
class MemberPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)

    # 명시적인 null 입력 거부
    @model_validator(mode="after")
    def reject_explicit_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


# 회원 조회 및 수정 후 반환할 데이터
class MemberResponse(BaseModel):
    member_id: int
    name: str
    email: EmailStr
    age: int


# ==================================
# 2. Database Functions
# ==================================

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


# ==================================
# 3. FastAPI Application
# ==================================

app = FastAPI(
    title="Chapter 08 - Member API",
    description="회원 등록, 조회 및 PUT/PATCH 수정 실습",
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
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT member_id
                FROM members
                WHERE email = %s;
                """,
                (str(member.email),),
            )

            if cursor.fetchone() is not None:
                raise HTTPException(
                    status_code=409,
                    detail="이미 등록된 이메일입니다.",
                )

            cursor.execute(
                """
                INSERT INTO members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING member_id, name, email, age;
                """,
                (member.name, str(member.email), member.age),
            )

            return cursor.fetchone()


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

            # 1. 회원 존재 확인
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

            # 3. 전체 수정
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

            updated = cursor.fetchone()
            conn.commit()

            return updated


# ==================================
# 6. PATCH - 회원 부분 수정 API
# ==================================

@app.patch(
    "/members/{member_id}",
    response_model=MemberResponse,
)
def patch_member(member_id: int, member: MemberPatch):

    # STEP 01. 실제 전달된 필드만 추출
    changes = member.model_dump(exclude_unset=True)

    # STEP 02. 빈 요청 확인
    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required",
        )

    with get_connection() as conn:
        with conn.cursor() as cursor:

            # STEP 03. 회원 존재 확인
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

            # STEP 04. 이메일 중복 확인
            if "email" in changes:
                cursor.execute(
                    """
                    SELECT member_id
                    FROM members
                    WHERE email = %s
                    AND member_id <> %s;
                    """,
                    (str(changes["email"]), member_id),
                )

                if cursor.fetchone() is not None:
                    raise HTTPException(
                        status_code=409,
                        detail="이미 등록된 이메일입니다.",
                    )

            # STEP 05. 허용된 컬럼만 선택
            allowed_fields = {
                "name": "name",
                "email": "email",
                "age": "age",
            }

            set_parts = []
            values = []

            for field, value in changes.items():
                column = allowed_fields[field]
                set_parts.append(f"{column} = %s")

                values.append(
                    str(value) if field == "email" else value
                )

            # WHERE 조건에 사용할 회원 ID 추가
            values.append(member_id)

            # STEP 06. 동적 UPDATE SQL 생성
            sql = f"""
                UPDATE members
                SET {', '.join(set_parts)}
                WHERE member_id = %s
                RETURNING member_id, name, email, age;
            """

            cursor.execute(sql, values)

            # STEP 07. 수정 결과 반환
            updated = cursor.fetchone()

            # STEP 08. 트랜잭션 확정
            conn.commit()

            return updated
