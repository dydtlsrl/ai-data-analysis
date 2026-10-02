-- Chapter 09. 09 (선택 실습) SQL 오류와 SAVEPOINT
-- 목적: 조건 불충족으로 인한 0행(정상)과 제약조건 위반으로 인한 SQL 오류(비정상)가
--       서로 다르다는 것, 그리고 오류 발생 후 SAVEPOINT로 일부만 되돌리는 방법을 관찰합니다.
-- 오류를 실제로 발생시키는 문장은 안전을 위해 기본적으로 주석 처리되어 있습니다.
-- 이 파일은 변경을 남기지 않으므로 06번 검증 결과에 영향을 주지 않습니다.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

BEGIN;

-- 오류가 날 수 있는 단계 이전에 SAVEPOINT를 만들어 둡니다.
SAVEPOINT before_optional_step;

-- 아래 INSERT의 주석을 해제하면 오류가 발생합니다.
-- 학생 103은 이미 강의 302에 '수강중' 상태로 신청되어 있으므로(주 실습 05 결과),
-- 같은 학생·강의 조합으로 '수강중'을 한 번 더 넣으려 하면
-- uq_transaction_enrollments_active 부분 고유 인덱스를 위반합니다.
--
-- INSERT INTO transaction_lab.enrollments (student_id, course_id, enrolled_at, status, recorded_amount)
-- VALUES (103, 302, CURRENT_TIMESTAMP, '수강중', 120000);
--
-- 예상 오류 메시지:
--   ERROR:  duplicate key value violates unique constraint "uq_transaction_enrollments_active"
--
-- 이 오류가 발생하면 현재 트랜잭션은 오류 상태(aborted)가 되고,
-- 이어지는 일반 SELECT도 다음과 같이 실패합니다.
--   ERROR:  current transaction is aborted, commands ignored until end of transaction block
--
-- 이때 기본 대응은 트랜잭션 전체를 ROLLBACK하는 것이지만,
-- SAVEPOINT를 미리 만들어 두었다면 그 지점까지만 되돌리고 트랜잭션을 계속할 수 있습니다.
-- (위 INSERT의 주석을 해제해 오류를 재현한 뒤, 아래 줄로 복구하세요.)
ROLLBACK TO SAVEPOINT before_optional_step;

-- 복구 후에는 트랜잭션이 정상 상태로 돌아와 이어서 실행할 수 있습니다.
SELECT 'savepoint recovery ok' AS note;

-- 이 실습은 실제 데이터를 바꾸지 않았으므로 COMMIT/ROLLBACK 어느 쪽이든 결과는 같습니다.
COMMIT;

-- 참고: 위 INSERT를 실제로 실행해 오류를 재현했다면,
--       오류 메시지 전체를 images/ 폴더에 캡처하고 chapter09_error_notes.md에 기록하세요.
