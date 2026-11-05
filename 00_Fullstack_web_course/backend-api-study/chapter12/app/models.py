
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Member(Base):
    # 실제 PostgreSQL 테이블 이름
    __tablename__ = "members"

    # 테이블 컬럼 매핑
    member_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
