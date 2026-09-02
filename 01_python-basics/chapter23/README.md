# Chapter 23 - 개인 지출 관리 프로그램

## 현재 완료

- 지출 추가
- 지출 목록 출력
- 전체 지출 합계
- 카테고리별 합계
- CSV 저장 / 불러오기
- 입력값 검증
  - 빈 값
  - 잘못된 금액
  - 날짜 형식
  - 파일 없음
- 메뉴 반복 실행
- pandas 교차 검증

## 현재 구조

### 공통으로 재사용할 함수
- calculate_total()
- calculate_by_category()

### Console 전용
- add_expense()
- show_expenses()

### CSV 전용
- save_expenses()
- load_expenses()

## 다음 작업

CSV 방식에서 PostgreSQL 방식으로 전환한다.

목표:

Console ─┐
         ├── PostgreSQL
Web ─────┘

- CSV 제거
- Console ↔ PostgreSQL 연결
- Web ↔ PostgreSQL 연결
- Console과 Web이 같은 DB 공유
- 공통 함수는 Console/Web에서 재사용

## 다음 시작 위치

STEP 24-1:
기존 함수에서 Console 전용 로직과 공통 비즈니스 로직을 분리한다.

특히 add_expense()의 input()/print()와
실제 지출 데이터 생성 로직을 어떻게 분리할지 확인한다.