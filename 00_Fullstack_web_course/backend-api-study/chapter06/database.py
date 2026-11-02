import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


# PostgreSQL 연결
def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        options=f"-c search_path={os.getenv('DB_SCHEMA', 'public')}",
        row_factory=dict_row,
    )


# 회원 전체 조회
def fetch_members():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT member_id, name, email, age
                FROM members
                ORDER BY member_id;
            """)
            return cur.fetchall()


# 회원 한 명 조회
def fetch_member_by_id(member_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT member_id, name, email, age
                FROM members
                WHERE member_id = %s;
            """, (member_id,))
            return cur.fetchone()


# 회원 등록
def insert_member(name: str, email: str, age: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING member_id, name, email, age;
            """, (name, email, age))
            return cur.fetchone()


# 회원 전체 수정
def update_member(member_id: int, name: str, email: str, age: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE members
                SET name = %s, email = %s, age = %s
                WHERE member_id = %s
                RETURNING member_id, name, email, age;
            """, (name, email, age, member_id))
            return cur.fetchone()


# 회원 일부 수정
def patch_member(member_id: int, changes: dict):
    fields = []
    values = []

    if "name" in changes:
        fields.append("name = %s")
        values.append(changes["name"])

    if "email" in changes:
        fields.append("email = %s")
        values.append(changes["email"])

    if "age" in changes:
        fields.append("age = %s")
        values.append(changes["age"])

    values.append(member_id)

    query = f"""
        UPDATE members
        SET {", ".join(fields)}
        WHERE member_id = %s
        RETURNING member_id, name, email, age;
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            return cur.fetchone()


# 회원 삭제
def delete_member(member_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM members
                WHERE member_id = %s
                RETURNING member_id, name, email, age;
            """, (member_id,))
            return cur.fetchone()