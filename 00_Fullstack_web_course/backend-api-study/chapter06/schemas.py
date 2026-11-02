from pydantic import BaseModel, Field


# 회원 등록 시 입력받을 데이터
class MemberCreate(BaseModel):
    name: str
    email: str
    age: int = Field(ge=0, le=150)


# 회원 전체 수정 시 입력받을 데이터
class MemberUpdate(BaseModel):
    name: str
    email: str
    age: int = Field(ge=0, le=150)


# 회원 일부 수정 시 입력받을 데이터
class MemberPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=1)
    age: int | None = Field(default=None, ge=0, le=150)


# 회원 정보를 반환할 데이터
class MemberResponse(BaseModel):
    member_id: int
    name: str
    email: str
    age: int