-- Chapter 09. 08 (선택 실습) 취소와 좌석 복구를 하나의 트랜잭션으로 처리하기
-- 목적: 수강중 → 취소 상태 전이와 좌석 복구를 별개로 실행하지 않고,
--       "취소에 실제로 성공한 행"만 좌석 복구의 입력으로 연결하는 패턴을 관찰합니다.
-- 이 파일은 주 실습(01~06)의 최종 상태를 보존하기 위해 마지막에 ROLLBACK합니다.
-- 즉 이 실습은 관찰용이며, 실행 후에도 06번 검증 결과는 그대로 유지됩니다.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

-- 취소 전 상태 확인 (기대: enrollment 9001 = 수강중, course 301 remaining_seats = 1)
SELECT * FROM transaction_lab.enrollments WHERE id = 9001;
SELECT course_id, remaining_seats FROM transaction_lab.course_inventory WHERE course_id = 301;

BEGIN;

-- 신청 9001을 취소하고, 그 취소가 실제로 적용된 경우에만(RETURNING이 비지 않을 때만)
-- 같은 강의의 좌석을 1개 복구합니다. 두 UPDATE를 나란히 실행하지 않고 CTE로 연결하는 이유는
-- 이미 취소된 신청을 다시 취소해도 좌석이 중복으로 늘어나지 않게 하기 위해서입니다.
WITH cancelled AS (
    UPDATE transaction_lab.enrollments
    SET status = '취소'
    WHERE id = 9001
      AND status = '수강중'
    RETURNING course_id
)
UPDATE transaction_lab.course_inventory AS ci
SET remaining_seats = ci.remaining_seats + 1
FROM cancelled AS e
WHERE ci.course_id = e.course_id
  AND ci.remaining_seats < ci.capacity;

-- 취소·복구 직후(트랜잭션 안) 임시 상태 확인
-- 기대: enrollment 9001 = 취소, course 301 remaining_seats = 2
SELECT * FROM transaction_lab.enrollments WHERE id = 9001;
SELECT course_id, remaining_seats FROM transaction_lab.course_inventory WHERE course_id = 301;

-- 검증: 취소 상태와 좌석 복구가 함께 반영되었는지 확인
DO $$
DECLARE
    v_status text;
    v_remaining int;
BEGIN
    SELECT status INTO v_status FROM transaction_lab.enrollments WHERE id = 9001;
    SELECT remaining_seats INTO v_remaining FROM transaction_lab.course_inventory WHERE course_id = 301;

    IF v_status IS DISTINCT FROM '취소' OR v_remaining <> 2 THEN
        RAISE EXCEPTION '취소·복구 검증 실패: status=%, remaining=%', v_status, v_remaining;
    END IF;

    RAISE NOTICE 'Chapter 09 cancel and restore (temporary) passed';
END
$$;

-- 이 선택 실습은 주 실습의 최종 상태(06번 검증 기준)를 보존하기 위해 ROLLBACK합니다.
-- 실제로 취소를 반영하고 싶다면 이 ROLLBACK을 COMMIT으로 바꾸되,
-- 그 경우 06_transaction_validation.sql의 기대값도 함께 다시 계산해야 합니다.
ROLLBACK;

-- ROLLBACK 후 상태가 06 실행 직후와 같은지 재확인 (기대: 수강중 / remaining_seats 1)
SELECT * FROM transaction_lab.enrollments WHERE id = 9001;
SELECT course_id, remaining_seats FROM transaction_lab.course_inventory WHERE course_id = 301;

-- 참고: 결제 환불(payments 테이블의 상태·금액 변경)은 이 장의 범위에 포함하지 않습니다.
-- 실제 서비스라면 환불 금액, 환불 상태, 승인 ID, 재시도/보상 처리를 위한 별도 구조가 필요합니다.
