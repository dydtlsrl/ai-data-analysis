from fastapi import APIRouter, HTTPException

from database import (
    delete_member,
    fetch_member_by_id,
    fetch_members,
    insert_member,
    patch_member,
    update_member as update_member_db,
)

from schemas import (
    MemberCreate,
    MemberPatch,
    MemberResponse,
    MemberUpdate,
)


router = APIRouter()


# 회원 전체 조회
@router.get("/members", response_model=list[MemberResponse])
def get_members():
    return fetch_members()


# 회원 한 명 조회
@router.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    member = fetch_member_by_id(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return member


# 회원 등록
@router.post(
    "/members",
    response_model=MemberResponse,
    status_code=201,
)
def create_member(member: MemberCreate):
    return insert_member(
        member.name,
        member.email,
        member.age,
    )


# 회원 전체 수정
@router.put("/members/{member_id}", response_model=MemberResponse)
def update_member_api(member_id: int, member: MemberUpdate):
    updated = update_member_db(
        member_id,
        member.name,
        member.email,
        member.age,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return updated


# 회원 일부 수정
@router.patch("/members/{member_id}", response_model=MemberResponse)
def patch_member_api(member_id: int, member: MemberPatch):
    changes = member.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided",
        )

    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422,
            detail="Fields cannot be null",
        )

    updated = patch_member(member_id, changes)

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return updated


# 회원 삭제
@router.delete("/members/{member_id}")
def remove_member(member_id: int):
    deleted = delete_member(member_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    return {
        "message": "Member deleted successfully",
        "member": deleted,
    }