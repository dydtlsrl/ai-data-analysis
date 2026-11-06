from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories import member_repository
from app.schemas import MemberCreate, MemberPatch, MemberUpdate


# 회원 생성 업무 규칙을 처리한다.
def create_member_service(db: Session, payload: MemberCreate):

    # 입력받은 이메일이 이미 DB에 존재하는지 조회한다.
    existing = member_repository.find_by_email(
        db,
        str(payload.email),
    )

    # 같은 이메일의 회원이 이미 있다면
    # 회원 생성을 진행하지 않고 409 Conflict 오류를 발생시킨다.
    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        # 중복이 아니라면 Repository에 실제 저장을 요청한다.
        return member_repository.create_member(
            db,
            payload.name,
            str(payload.email),
            payload.age,
        )

    except IntegrityError:
        # DB의 UNIQUE 제약으로 중복이 확인되면
        # 클라이언트가 이해할 수 있는 409 Conflict로 변환한다.
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )


# 회원 번호를 받아 회원 삭제 업무 규칙을 처리한다.
def delete_member_service(db: Session, member_id: int):

    # 삭제할 회원이 실제로 존재하는지 조회한다.
    member = member_repository.find_by_id(db, member_id)

    # 해당 회원이 없으면 삭제를 진행하지 않고 404 오류를 발생시킨다.
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    # 회원이 존재하면 Repository에 실제 삭제를 요청한다.
    member_repository.delete_member(db, member)

    # 전체 회원 목록을 조회하는 업무를 처리한다.
def get_members_service(db: Session):

    # Repository에 전체 회원 조회를 요청하고 결과를 반환한다.
    return member_repository.find_all(db)


# 회원 번호로 회원 한 명을 조회하는 업무를 처리한다.
def get_member_service(db: Session, member_id: int):

    # Repository에 회원 한 명 조회를 요청한다.
    member = member_repository.find_by_id(db, member_id)

    # 해당 회원이 없으면 404 Not Found 오류를 발생시킨다.
    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    # 조회된 Member 객체를 반환한다.
    return member


    # 회원 정보를 전체 수정하는 업무 규칙을 처리한다.
def update_member_service(
    db: Session,
    member_id: int,
    payload: MemberUpdate,
):
    # 수정할 회원이 존재하는지 확인한다.
    # 없으면 get_member_service()가 404 오류를 발생시킨다.
    member = get_member_service(db, member_id)

    # 새로 입력한 이메일이 다른 회원에게 이미 사용 중인지 조회한다.
    existing = member_repository.find_by_email(
        db,
        str(payload.email),
    )

    # 이메일을 사용 중인 회원이 있고,
    # 그 회원이 현재 수정 중인 회원이 아니라면 중복이다.
    if existing is not None and existing.member_id != member.member_id:
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )

    try:
        # 중복이 없다면 Repository에 전체 수정을 요청한다.
        return member_repository.update_member(
            db,
            member,
            payload,
        )

    except IntegrityError:
        # 동시에 같은 이메일이 저장되는 상황 등에서
        # DB 제약 오류가 발생하면 409로 변환한다.
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )



        # 회원 정보 중 요청에서 전달한 필드만 수정하는 업무 규칙을 처리한다.
def patch_member_service(
    db: Session,
    member_id: int,
    payload: MemberPatch,
):
    # 요청에서 실제로 전달된 필드만 추출한다.
    changes = payload.model_dump(exclude_unset=True)

    # 아무 필드도 전달하지 않은 빈 PATCH 요청은 거부한다.
    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required",
        )

    # 수정할 회원이 존재하는지 확인한다.
    # 없으면 get_member_service()가 404 오류를 발생시킨다.
    member = get_member_service(db, member_id)

    # 이메일 변경이 포함된 경우에만 중복을 확인한다.
    if "email" in changes:
        existing = member_repository.find_by_email(
            db,
            str(changes["email"]),
        )

        # 같은 이메일을 다른 회원이 사용 중이면 409 오류를 발생시킨다.
        if existing is not None and existing.member_id != member.member_id:
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            )

    try:
        # 전달된 필드만 수정하도록 Repository에 요청한다.
        return member_repository.patch_member(
            db,
            member,
            payload,
        )

    except IntegrityError:
        # 동시 요청 등으로 DB에서 이메일 중복이 발생하면
        # API 의미에 맞는 409 오류로 변환한다.
        raise HTTPException(
            status_code=409,
            detail="Email already exists",
        )