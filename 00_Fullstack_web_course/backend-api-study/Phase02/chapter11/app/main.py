
from sqlalchemy import select

from .db import SessionLocal
from .models import Member


# 전체 회원 조회
def get_members():
    with SessionLocal() as session:
        stmt = select(Member).order_by(Member.member_id)
        members = session.scalars(stmt).all()

        for member in members:
            print(
                member.member_id,
                member.name,
                member.email,
                member.age,
            )


# 특정 회원 조회
def get_member_by_id(member_id: int):
    with SessionLocal() as session:
        stmt = select(Member).where(
            Member.member_id == member_id
        )

        member = session.scalar(stmt)

        if member is None:
            print("회원 정보를 찾을 수 없습니다.")
            return

        print(
            member.member_id,
            member.name,
            member.email,
            member.age,
        )


if __name__ == "__main__":
    print("===== 존재하지 않는 회원 조회 =====")
    get_member_by_id(999999)
