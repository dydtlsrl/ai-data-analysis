import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

def check_connection():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT current_database(), current_schema();"
            )
            return cur.fetchone()


def fetch_members():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT member_id, name, email, age
                FROM practice.members
                ORDER BY member_id;
                """
            )
            return cur.fetchall()