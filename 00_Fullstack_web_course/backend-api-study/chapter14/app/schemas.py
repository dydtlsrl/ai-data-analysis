from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


# 회원 생성 요청에서 입력받을 데이터 형식을 정의한다.
class MemberCreate(BaseModel):

    # 이름은 반드시 입력하며, 1~100자만 허용한다.
    name: str = Field(min_length=1, max_length=100)

    # 올바른 이메일 형식인지 자동으로 검사한다.
    email: EmailStr

    # 나이는 0~150 범위의 정수만 허용한다.
    age: int = Field(ge=0, le=150)

    # 회원 전체 수정 요청에서 입력받을 데이터 형식을 정의한다.
class MemberUpdate(BaseModel):

    # 이름은 반드시 입력하며, 1~100자만 허용한다.
    name: str = Field(min_length=1, max_length=100)

    # 올바른 이메일 형식인지 자동으로 검사한다.
    email: EmailStr

    # 나이는 0~150 범위의 정수만 허용한다.
    age: int = Field(ge=0, le=150)


# 회원 일부 수정 요청에서 입력받을 데이터 형식을 정의한다.
class MemberPatch(BaseModel):

    # 이름은 생략 가능하다.
    # 단, 전달했다면 1~100자여야 한다.
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    # 이메일은 생략 가능하다.
    # 단, 전달했다면 올바른 이메일 형식이어야 한다.
    email: EmailStr | None = None

    # 나이는 생략 가능하다.
    # 단, 전달했다면 0~150 범위여야 한다.
    age: int | None = Field(
        default=None,
        ge=0,
        le=150,
    )

    # 클라이언트가 필드를 아예 보내지 않은 것은 허용한다.
    # 하지만 null을 명시적으로 보낸 것은 거부한다.
    @model_validator(mode="after")
    def reject_explicit_null(self):
        # 실제 요청에 포함된 필드만 확인한다.
        for field in self.model_fields_set:

            # 요청에 포함된 값이 None이면 Validation 오류를 발생시킨다.
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")

        # 검증이 통과한 현재 객체를 반환한다.
        return self


        # 회원 정보를 API 응답으로 반환할 데이터 형식을 정의한다.
class MemberResponse(BaseModel):

    # SQLAlchemy ORM 객체의 속성을 읽어
    # Pydantic 응답 객체로 변환할 수 있게 설정한다.
    model_config = ConfigDict(from_attributes=True)

    # 회원 번호를 응답에 포함한다.
    member_id: int

    # 회원 이름을 응답에 포함한다.
    name: str

    # 회원 이메일을 응답에 포함한다.
    email: str

    # 회원 나이를 응답에 포함한다.
    age: int