from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Member
from app.schemas import MemberPatch, MemberUpdate


# members 테이블의 모든 회원을 조회한다.
def find_all(db: Session):
    # Member 전체를 선택하고 회원 번호 순서로 정렬하는
    # SELECT 문을 만든다.
    stmt = select(Member).order_by(Member.member_id)

    # SELECT 문을 실행하고,
    # 조회된 Member 객체를 모두 리스트로 반환한다.
    return db.scalars(stmt).all()


# 전달받은 회원 번호로 회원 한 명을 조회한다.
def find_by_id(db: Session, member_id: int):
    # Member의 기본키에서 member_id와 일치하는 객체를 찾는다.
    # 회원이 없으면 None을 반환한다.
    return db.get(Member, member_id)


# 전달받은 이메일과 일치하는 회원을 조회한다.
def find_by_email(db: Session, email: str):
    # members 테이블에서 email이 전달받은 값과
    # 일치하는 회원을 조회하는 SELECT 문을 만든다.
    stmt = select(Member).where(Member.email == email)

    # 회원 한 명 또는 None을 반환한다.
    return db.scalar(stmt)


# 전달받은 회원 정보로 새로운 회원을 생성한다.
def create_member(
    db: Session,
    name: str,
    email: str,
    age: int,
):
    # 전달받은 값으로 새로운 Member 객체를 만든다.
    member = Member(
        name=name,
        email=email,
        age=age,
    )

    try:
        # 새 Member 객체를 Session의 관리 대상으로 등록한다.
        db.add(member)

        # 변경 내용을 DB에 최종 확정한다.
        db.commit()

        # DB에 저장된 최신 값을 객체에 다시 반영한다.
        db.refresh(member)

        # 저장된 Member 객체를 반환한다.
        return member

    except IntegrityError:
        # 이메일 중복 등 DB 무결성 오류가 발생하면
        # 현재 Transaction을 취소한다.
        db.rollback()

        # Service가 409 오류로 변환하도록 예외를 다시 전달한다.
        raise

    except Exception:
        # 그 외 오류가 발생해도 현재 Transaction을 취소한다.
        db.rollback()
        raise


# 기존 회원의 모든 정보를 전달받은 값으로 수정한다.
def update_member(
    db: Session,
    member: Member,
    payload: MemberUpdate,
):
    # 기존 Member 객체의 모든 값을 새 값으로 교체한다.
    member.name = payload.name
    member.email = str(payload.email)
    member.age = payload.age

    try:
        # 변경 내용을 DB에 최종 확정한다.
        db.commit()

        # DB에 반영된 최신 값을 객체에 다시 불러온다.
        db.refresh(member)

        return member

    except Exception:
        # 수정 실패 시 변경 작업을 취소한다.
        db.rollback()
        raise


# 전달받은 필드만 기존 회원 정보에 반영한다.
def patch_member(
    db: Session,
    member: Member,
    payload: MemberPatch,
):
    # 요청에서 실제로 전달된 필드만 추출한다.
    changes = payload.model_dump(exclude_unset=True)

    # 전달된 필드만 하나씩 수정한다.
    for field, value in changes.items():
        # 이메일은 일반 문자열로 변환한다.
        if field == "email":
            value = str(value)

        # field 이름에 해당하는 Member 속성을 수정한다.
        setattr(member, field, value)

    try:
        # 변경 내용을 DB에 최종 확정한다.
        db.commit()

        # DB에 반영된 최신 값을 객체에 다시 불러온다.
        db.refresh(member)

        return member

    except Exception:
        # 수정 실패 시 변경 작업을 취소한다.
        db.rollback()
        raise


# 전달받은 Member 객체를 데이터베이스에서 삭제한다.
def delete_member(db: Session, member: Member):
    try:
        # 삭제할 객체를 Session에 등록한다.
        db.delete(member)

        # 삭제 작업을 DB에 최종 확정한다.
        db.commit()

    except Exception:
        # 삭제 실패 시 변경 작업을 취소한다.
        db.rollback()
        raise