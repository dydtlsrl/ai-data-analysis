from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    MemberCreate,
    MemberPatch,
    MemberResponse,
    MemberUpdate,
)

from app.services import member_service


# /members로 시작하는 회원 관련 URL을 관리하는 Router를 만든다.
router = APIRouter(
    prefix="/members",
    tags=["members"],
)


# GET /members 요청을 받으면 전체 회원 목록을 반환한다.
@router.get(
    "/",
    response_model=list[MemberResponse],
)
def get_members(
    # FastAPI가 요청마다 get_db()를 실행해 DB Session을 전달한다.
    db: Session = Depends(get_db),
):
    # Service에 전체 회원 조회를 요청하고 결과를 반환한다.
    return member_service.get_members_service(db)


# GET /members/회원번호 요청을 받으면 회원 한 명을 반환한다.
@router.get(
    "/{member_id}",
    response_model=MemberResponse,
)
def get_member(
    # URL의 회원 번호를 정수로 받는다.
    member_id: int,

    # FastAPI가 요청마다 DB Session을 전달한다.
    db: Session = Depends(get_db),
):
    # Service에 회원 한 명 조회를 요청하고 결과를 반환한다.
    # 회원이 없으면 Service가 404 오류를 발생시킨다.
    return member_service.get_member_service(db, member_id)


# POST /members/ 요청을 받으면 새 회원을 생성한다.
@router.post(
    "/",
    response_model=MemberResponse,
    status_code=201,
)
def create_member(
    # 요청 JSON을 MemberCreate 규칙으로 검증해 받는다.
    payload: MemberCreate,

    # FastAPI가 요청마다 DB Session을 전달한다.
    db: Session = Depends(get_db),
):
    # Service에 회원 생성 업무 처리를 요청한다.
    # 중복 이메일이면 Service가 409 오류를 발생시킨다.
    return member_service.create_member_service(db, payload)


# PUT /members/회원번호 요청을 받으면 회원 정보를 전체 수정한다.
@router.put(
    "/{member_id}",
    response_model=MemberResponse,
)
def update_member(
    # URL에서 수정할 회원 번호를 정수로 받는다.
    member_id: int,

    # 요청 JSON을 MemberUpdate 규칙으로 검증해 받는다.
    payload: MemberUpdate,

    # FastAPI가 요청마다 DB Session을 전달한다.
    db: Session = Depends(get_db),
):
    # Service에 회원 전체 수정 업무를 요청한다.
    # 회원이 없으면 404, 이메일이 중복되면 409를 반환한다.
    return member_service.update_member_service(
        db,
        member_id,
        payload,
    )


# PATCH /members/회원번호 요청을 받으면 전달된 필드만 수정한다.
@router.patch(
    "/{member_id}",
    response_model=MemberResponse,
)
def patch_member(
    member_id: int,
    payload: MemberPatch,
    db: Session = Depends(get_db),
):
    # Service에 일부 수정 업무를 요청한다.
    return member_service.patch_member_service(
        db,
        member_id,
        payload,
    )


# DELETE /members/회원번호 요청을 받으면 회원을 삭제한다.
@router.delete(
    "/{member_id}",
    status_code=204,
)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    # Service에 회원 삭제 업무를 요청한다.
    member_service.delete_member_service(
        db,
        member_id,
    )