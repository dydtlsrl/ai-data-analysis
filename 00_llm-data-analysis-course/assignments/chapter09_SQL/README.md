# Chapter 09 실습 코드

## 트랜잭션으로 데이터 정합성 지키기

이 폴더는 Chapter 07에서 완성한 `course_project` 데이터를 변경하지 않고, 별도의 `transaction_lab` 스키마에서 **BEGIN·COMMIT·ROLLBACK**과 좌석·신청·결제의 원자적 처리를 실습하는 SQL 파일을 관리합니다.

출처: [아토믹데브(dev-dog) 블로그 — Chapter 09. 트랜잭션으로 데이터 정합성 지키기](https://blog.naver.com/dev-dog/224394079809)

## 실행 전 조건

Chapter 07·08의 다음 파일을 순서대로 실행해 기준 상태를 만들어 둡니다.

```text
chapter07/01_course_project_schema.sql
→ chapter07/02_course_project_seed.sql
→ chapter07/03_course_project_changes.sql
→ chapter07/04_course_project_validation.sql
→ chapter08_SQL/00_check_course_project.sql
```

기준 상태:

```text
students 3 / instructors 2 / courses 3 / enrollments 5
1001 완료 / 100000
1004 취소 / 150000
1005 신청 / 120000
전체 590000 / 활성 340000 / 취소 제외 440000
```

## 왜 별도 스키마를 쓰는가

기존 `course_project` 테이블을 다시 만들거나 데이터를 바꾸면 Chapter 07·08의 기준 상태가 손상됩니다. Chapter 09는 좌석·트랜잭션 실험 상태만 담는 `transaction_lab` 스키마를 따로 두고, 학생·강의 마스터는 `course_project`를 FK로 참조합니다.

```text
transaction_lab.course_inventory.course_id  → course_project.courses.id
transaction_lab.enrollments.student_id      → course_project.students.id
transaction_lab.enrollments.course_id       → course_project.courses.id
transaction_lab.payments.enrollment_id      → transaction_lab.enrollments.id
```

## 파일 목록과 실행 순서

주 실습(반드시 순서대로 실행):

```text
01_transaction_lab_schema.sql
→ 02_transaction_lab_seed.sql
→ 03_commit_transaction.sql
→ 04_rollback_transaction.sql
→ 05_commit_and_sold_out.sql
→ 06_transaction_validation.sql
```

| 파일 | 설명 |
| --- | --- |
| `01_transaction_lab_schema.sql` | Chapter 07/08 기준 상태 사전 검사 + `transaction_lab` 스키마·3테이블·활성 신청 인덱스 생성 (DDL도 하나의 트랜잭션) |
| `02_transaction_lab_seed.sql` | 강의 301/302/303 좌석(`capacity`/`remaining_seats`) 초기 입력 |
| `03_commit_transaction.sql` | 학생 101 + 강의 301: 좌석 잠금(`FOR UPDATE`) → 조건부 차감 → 신청·결제 생성 → 검증 → `COMMIT` |
| `04_rollback_transaction.sql` | 학생 102 + 강의 302: 같은 흐름을 만든 뒤 결제 승인 실패를 가정하고 `ROLLBACK` |
| `05_commit_and_sold_out.sql` | 학생 103 + 강의 302 정상 `COMMIT`(좌석 소진) + 추가 신청의 조건부 UPDATE가 0행으로 끝나는 것을 확인 + IDENTITY 다음 값 정리 |
| `06_transaction_validation.sql` | 좌석 범위, 결제 누락, 금액 불일치, 고아 결제, 중복 활성 신청, 활성 신청 수 = 사용 좌석 수를 자동 판정하는 완료 게이트 |

선택 실습(개념 확인용, 최종 상태에 영향 없음):

| 파일 | 설명 |
| --- | --- |
| `07_concurrency_two_sessions.sql` | 두 개의 DBeaver 연결로 강의 303의 `FOR UPDATE` Lock 대기를 관찰 (파일 자체는 실행 안내문) |
| `08_cancel_and_restore.sql` | 신청 9001 취소 + 좌석 복구를 CTE로 연결, 관찰 후 `ROLLBACK`으로 최종 상태 보존 |
| `09_error_and_savepoint.sql` | 중복 활성 신청으로 인한 제약조건 오류와 `SAVEPOINT` 복구(오류 유발 문장은 기본 주석 처리) |

정리용:

| 파일 | 설명 |
| --- | --- |
| `reset_transaction_lab.sql` | `transaction_lab` 스키마만 삭제(재실습용). `course_project`는 건드리지 않음 |

## 초기 좌석 상태 (02 실행 직후)

| course_id | 강의 | 가격 | capacity | remaining_seats |
| ---: | --- | ---: | ---: | ---: |
| 301 | 데이터베이스 입문 | 100000 | 2 | 2 |
| 302 | 정규화 실습 | 120000 | 1 | 1 |
| 303 | 파이썬 데이터 분석 | 150000 | 1 | 1 |

## 최종 기대 상태 (06 실행 시점)

```text
course_project.enrollments = 5 (변경 없음)
transaction_lab.enrollments = 2 (9001, 9002)
transaction_lab.payments = 2 (9901, 9902)
course 301 remaining_seats = 1
course 302 remaining_seats = 0
course 303 remaining_seats = 1
```

통과 메시지:

```text
Chapter 09 main transaction validation passed
```

## 핵심 개념 정리

**BEGIN / COMMIT / ROLLBACK**

```text
BEGIN    → 현재 세션에서 트랜잭션 시작
COMMIT   → 검증이 끝난 뒤 변경 확정
ROLLBACK → 오류·검증 실패 시 아직 확정되지 않은 변경 취소
```

**조건부 UPDATE 0행 ≠ SQL 오류**

좌석이 없어 `UPDATE ... WHERE remaining_seats > 0`이 0행을 반환하는 것은 정상 실행 결과(업무상 "정원 마감")입니다. PostgreSQL 문법 오류나 자동 ROLLBACK이 아니며, CTE로 연결된 후속 INSERT도 함께 0건이 됩니다(`05_commit_and_sold_out.sql`).

**SQL 오류와 SAVEPOINT**

제약조건 위반 같은 실제 오류는 트랜잭션을 오류 상태(aborted)로 만들고, 이후 문장은 `current transaction is aborted`로 모두 실패합니다. 기본 대응은 `ROLLBACK`이며, 일부만 되돌리려면 오류 전에 미리 `SAVEPOINT`를 만들어 둡니다(`09_error_and_savepoint.sql`).

**ROLLBACK과 IDENTITY 번호는 다르다**

이 실습은 결과 비교를 위해 신청/결제 ID를 명시적으로 입력합니다(9001, 9002 …). ROLLBACK된 명시적 ID는 다시 사용할 수 있지만(`04`→`05`에서 9002/9902 재사용), IDENTITY 자동 번호는 트랜잭션이 취소되어도 일반적으로 회수되지 않습니다.

**FOR UPDATE와 조건부 UPDATE**

`SELECT ... FOR UPDATE`는 대상 행을 잠근 상태로 관찰합니다. `UPDATE ... WHERE remaining_seats > 0 ... RETURNING`은 그 자체로도 수정 대상 행에 필요한 잠금을 얻으므로, 단일 조건부 변경만 필요하다면 선행 `FOR UPDATE`가 항상 필수는 아닙니다. 이 실습은 좌석 행을 잠근 상태로 먼저 관찰하는 흐름과 두 세션 대기를 명확히 보여주기 위해 `FOR UPDATE`를 함께 사용합니다.

**Lock 대기와 Deadlock**

한 트랜잭션이 다른 트랜잭션의 잠금 해제를 기다리는 것은 일반적인 Lock 대기입니다. Deadlock은 두 트랜잭션이 서로의 잠금을 순환 구조로 기다리는 경우이며, PostgreSQL은 이를 감지하면 한 트랜잭션을 오류로 종료합니다.

## 실행 방법과 주의사항

- 이 실습은 같은 DBeaver SQL Editor(같은 연결 세션)에서 문장 순서대로 실행합니다. 다른 연결에서 COMMIT/ROLLBACK을 실행해도 현재 트랜잭션을 제어할 수 없습니다.
- `07_concurrency_two_sessions.sql`만 예외적으로 두 개의 연결(SQL Editor 탭)을 각각 열어 파일 안의 지시대로 번갈아 실행합니다.
- 모든 파일은 `course_project.table_name`, `transaction_lab.table_name` 형식의 스키마 한정 이름을 사용하므로 `current_schema()`가 `transaction_lab`일 필요는 없습니다.
- 오류가 발생하면 화면을 캡처해 `images/`에 저장하고, `chapter09_error_notes.md`에 오류 핵심·원인·해결 과정을 기록합니다.
