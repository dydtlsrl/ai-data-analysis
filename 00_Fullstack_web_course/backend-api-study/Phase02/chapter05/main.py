from db import check_connection, fetch_members


if __name__ == "__main__":
    try:
        # DB 연결 확인
        database, schema = check_connection()

        print("DB 연결 성공!")
        print(f"Database: {database}")
        print(f"Schema: {schema}")

        # 회원 목록 조회
        print("\n회원 목록 조회:")

        members = fetch_members()

        for member in members:
            print(member)

    except Exception as e:
        print(f"DB 연결 실패: {e}")