# Chapter 09 오류 기록

### 오류 1: `23505 중복 활성 신청 / 25P02 트랜잭션 중지`

- **발생 파일**: `09_error_and_savepoint.sql`의 주석 처리된 중복 INSERT를 별도 psql 입력에서 실행.
- **발생 상황**: 학생 103의 강의 302 수강중 신청이 이미 존재하는 상태에서 중복 신청을 입력했다. 저장점 이후 임시 좌석 차감도 추가하여 복구 범위를 확인했다.

**실행한 코드**

```sql
BEGIN;
SAVEPOINT before_optional_step;
UPDATE transaction_lab.course_inventory
SET remaining_seats = remaining_seats - 1 WHERE course_id = 303;
INSERT INTO transaction_lab.enrollments
(student_id, course_id, enrolled_at, status, recorded_amount)
VALUES (103, 302, CURRENT_TIMESTAMP, '수강중', 120000);
SELECT 'after error';
ROLLBACK TO SAVEPOINT before_optional_step;
SELECT 'savepoint recovery ok' AS note;
SELECT course_id, remaining_seats
FROM transaction_lab.course_inventory WHERE course_id = 303;
COMMIT;
```

**발생한 오류 메시지**

```text
오류:  23505: 중복된 키 값이 "uq_transaction_enrollments_active" 고유 제약 조건을 위반함
DETAIL:  (student_id, course_id)=(103, 302) 키가 이미 있습니다.
오류:  25P02: 현재 트랜잭션은 중지되어 있습니다. 이 트랜잭션을 종료하기 전까지는 모든 명령이 무시될 것입니다
```

**오류 화면 캡처**

이 오류는 psql에서 재현했다. DBeaver 오류 화면 캡처는 없으며, [실제 오류와 복구 원본 출력](logs/09_savepoint_error.txt)을 증거로 연결한다.

**오류 핵심 요약**

같은 학생·강의의 중복 활성 신청이 부분 고유 인덱스에 의해 거부됐다. 이후 열린 트랜잭션이 오류 상태여서 SELECT도 거부됐다.

**원인 설명**

`(student_id, course_id) WHERE status = '수강중'` 조건의 고유 인덱스가 중복을 방지한다. SQL 오류가 발생한 트랜잭션은 ROLLBACK 또는 저장점 복구 전까지 계속 실행할 수 없다.

**해결 방법 — 예상**

사전에 만든 SAVEPOINT로 되돌리면 오류 이후 변경을 취소하고 트랜잭션을 계속 사용할 수 있을 것으로 예상했다.

**해결 방법 — 실제로 해결한 방법**

`ROLLBACK TO SAVEPOINT before_optional_step` 실행 후 `savepoint recovery ok` 조회에 성공했다. 임시 차감한 303 좌석은 1로 복구되었고 COMMIT에 성공했다. 중복 신청은 추가되지 않았다. 자동 번호 9003은 오류에도 소비되어 신청 시퀀스는 9003/true, 다음 값은 9004다. 결제 시퀀스는 9903/false를 유지했다.

**같은 오류가 다시 나면 확인할 체크리스트**

| 증상 | 원인 체크리스트 | 해결 |
| --- | --- | --- |
| 23505 | 동일 학생·강의의 수강중 신청이 존재하는가 | 중복 신청을 막고 트랜잭션을 복구한다 |
| 25P02 | 앞선 문장에서 오류가 발생했는가 | 저장점이 있으면 ROLLBACK TO SAVEPOINT, 없으면 ROLLBACK한다 |
| 자동 번호 누락 | 실패한 INSERT에서 nextval이 호출됐는가 | 번호 연속성 대신 실제 행과 관계를 검증한다 |