-- Chapter 09. 04 실패를 가정한 ROLLBACK
-- 시작 상태: course 302 remaining_seats 1, lab enrollments/payments는 03의 결과만 있음(1행씩)
-- 완료 상태: ROLLBACK으로 03 실행 직후 상태와 동일하게 되돌아감 (course 302 remaining_seats 1 유지)
-- 학생 102가 강의 302를 신청하는 변경을 만든 뒤, 외부 결제 승인 실패를 가정하고 취소합니다.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

BEGIN;

-- 03과 동일한 패턴: 좌석 차감 → 신청 생성 → 결제 생성을 연결합니다.
-- 여기서는 결과를 COMMIT하지 않고 임시 상태만 관찰할 목적입니다.
WITH seat AS (
    UPDATE transaction_lab.course_inventory AS ci
    SET remaining_seats = ci.remaining_seats - 1
    FROM course_project.courses AS c
    WHERE ci.course_id = c.id
      AND ci.course_id = 302
      AND ci.remaining_seats > 0
    RETURNING ci.course_id, c.price
),
new_enrollment AS (
    INSERT INTO transaction_lab.enrollments (
        id, student_id, course_id,
        enrolled_at, status, recorded_amount
    )
    SELECT
        9002, 102, course_id,
        CURRENT_TIMESTAMP, '수강중', price
    FROM seat
    RETURNING id, recorded_amount
)
INSERT INTO transaction_lab.payments (
    id, enrollment_id, amount, paid_at
)
SELECT
    9902, id, recorded_amount, CURRENT_TIMESTAMP
FROM new_enrollment
RETURNING id, enrollment_id, amount;

-- ROLLBACK 전 임시 상태 확인(같은 트랜잭션 안에서는 이 변경이 보입니다).
-- 기대: course 302 remaining_seats 0, enrollment 9002 존재, payment 9902 존재
SELECT course_id, remaining_seats FROM transaction_lab.course_inventory WHERE course_id = 302;
SELECT * FROM transaction_lab.enrollments WHERE id = 9002;
SELECT * FROM transaction_lab.payments WHERE id = 9902;

-- 외부 결제 승인 실패를 가정하고 트랜잭션 전체를 취소합니다.
ROLLBACK;

-- ROLLBACK 후 상태 확인
-- 기대: course 302 remaining_seats 1(복구), enrollment 9002 없음, payment 9902 없음
SELECT course_id, remaining_seats FROM transaction_lab.course_inventory WHERE course_id = 302;
SELECT * FROM transaction_lab.enrollments WHERE id = 9002;
SELECT * FROM transaction_lab.payments WHERE id = 9902;

-- ROLLBACK 후 상태를 코드로도 검증합니다(자동 실행, 별도 트랜잭션).
DO $$
DECLARE
    v_remaining_seats int;
    v_enrollment_count bigint;
    v_payment_count bigint;
BEGIN
    SELECT remaining_seats INTO v_remaining_seats
    FROM transaction_lab.course_inventory WHERE course_id = 302;

    SELECT COUNT(*) INTO v_enrollment_count
    FROM transaction_lab.enrollments WHERE id = 9002;

    SELECT COUNT(*) INTO v_payment_count
    FROM transaction_lab.payments WHERE id = 9902;

    IF v_remaining_seats <> 1 OR v_enrollment_count <> 0 OR v_payment_count <> 0 THEN
        RAISE EXCEPTION
            'ROLLBACK 검증 실패: remaining=%, enrollment=%, payment=%',
            v_remaining_seats, v_enrollment_count, v_payment_count;
    END IF;

    RAISE NOTICE 'Chapter 09 rollback transaction (course 302) passed';
END
$$;
