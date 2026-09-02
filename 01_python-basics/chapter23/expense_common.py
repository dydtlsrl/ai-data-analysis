import csv #표 형태의 데이터를 파일로 저장하는 간단한 형식
from pathlib import Path
import pandas as pd
from datetime import datetime


def create_expense(date, category, description, amount):

    # 빈 값 검사
    if not date or not category or not description:
        return None, "날짜, 카테고리, 내용은 비워 둘 수 없습니다."
    # 날짜 형식 검사
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return None, "날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식을 사용해주세요."
    # amount 정수 변환 검사
    try:
        amount = int(amount)
    except ValueError:
        return None, "금액은 숫자로 입력해주세요."
    # amount가 0보다 큰지 검사
    if amount <= 0:
        return None, "금액은 0보다 커야 합니다."
    # expense 딕셔너리 생성
    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount,
    }
    # return
    # return expense, "성공적으로 지출이 추가되었습니다."
    return expense, None
# 출력 테스트
# expense, error = create_expense(
#     "2026-09-01",
#     "식비",
#     "점심",
#     "12000"
# )

# print(expense)
# print(error)

# Error 테스트
# expense, error = create_expense(
#     "2026-99-01",
#     "식비",
#     "점심",
#     "12000"
# )

# print(expense)
# print(error)