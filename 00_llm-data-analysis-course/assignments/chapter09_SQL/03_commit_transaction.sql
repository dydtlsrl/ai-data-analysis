-- Chapter 09. 03 성공 트랜잭션 — 좌석·신청·결제를 함께 확정한다
-- 시작 상태: course 301 remaining_seats 2, lab enrollments/payments 0행
-- 완료 상태: course 301 remaining_seats 1, enrollment 9001(수강중), payment 9901 COMMIT
-- 학생 101이 강의 301을 신청하는 사례입니다.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

BEGIN;

-- 1) 좌석 상태 행을 잠근 상태로 읽어 최신 remaining_seats를 확인합니다.
--    FOR UPDATE OF ci는 이 행을 다른 트랜잭션이 동시에 수정하지 못하게 잠급니다.
SELECT
    ci.course_id,
    c.title,
    c.price,
    ci.remaining_seats
FROM transaction_lab.course_inventory AS ci
JOIN course_project.courses AS c
    ON c.id = ci.course_id
WHERE ci.course_id = 301
FOR UPDATE OF ci;

-- 2) 조건부 좌석 차감 → 신청 생성 → 결제 생성을 하나의 문장으로 연결합니다.
--    seat 좌석 UPDATE가 0행이면 new_enrollment도 비고, 결제 INSERT도 실행되지 않습니다.
--    즉 좌석이 실제로 있을 때만 신청·결제가 함께 만들어집니다(원자적 처리).
WITH seat AS (
    UPDATE transaction_lab.course_inventory AS ci
    SET remaining_seats = ci.remaining_seats - 1
    FROM course_project.courses AS c
    WHERE ci.course_id = c.id
      AND ci.course_id = 301
      AND ci.remaining_seats > 0
    RETURNING ci.course_id, c.price
),
new_enrollment AS (
    INSERT INTO transaction_lab.enrollments (
        id, student_id, course_id,
        enrolled_at, status, recorded_amount
    )
    SELECT
        9001, 101, course_id,
        CURRENT_TIMESTAMP, '수강중', price
    FROM seat
    RETURNING id, recorded_amount
)
INSERT INTO transaction_lab.payments (
    id, enrollment_id, amount, paid_at
)
SELECT
    9901, id, recorded_amount, CURRENT_TIMESTAMP
FROM new_enrollment
RETURNING id, enrollment_id, amount;

-- 3) COMMIT 전 검증: 신청 1행, 결제 1행, 금액 일치, 좌석 1행 감소를 확인합니다.
--    하나라도 다르면 예외를 발생시켜 COMMIT 이전에 트랜잭션이 중단됩니다.
DO $$
DECLARE
    v_enrollment_count bigint;
    v_payment_count bigint;
    v_enrollment_amount numeric;
    v_payment_amount numeric;
    v_remaining_seats int;
BEGIN
    SELECT COUNT(*) INTO v_enrollment_count
    FROM transaction_lab.enrollments WHERE id = 9001;

    SELECT COUNT(*) INTO v_payment_count
    FROM transaction_lab.payments WHERE id = 9901;

    SELECT recorded_amount INTO v_enrollment_amount
    FROM transaction_lab.enrollments WHERE id = 9001;

    SELECT amount INTO v_payment_amount
    FROM transaction_lab.payments WHERE id = 9901;

    SELECT remaining_seats INTO v_remaining_seats
    FROM transaction_lab.course_inventory WHERE course_id = 301;

    IF v_enrollment_count <> 1
       OR v_payment_count <> 1
       OR v_enrollment_amount <> 100000
       OR v_payment_amount <> 100000
       OR v_enrollment_amount IS DISTINCT FROM v_payment_amount
       OR v_remaining_seats <> 1 THEN
        RAISE EXCEPTION
            '성공 트랜잭션 검증 실패: enrollment=%, payment=%, enrollment_amount=%, payment_amount=%, remaining=%',
            v_enrollment_count, v_payment_count, v_enrollment_amount, v_payment_amount, v_remaining_seats;
    END IF;

    RAISE NOTICE 'Chapter 09 commit transaction (course 301) passed';
END
$$;

COMMIT;

-- COMMIT 후 최종 상태 확인
SELECT course_id, remaining_seats FROM transaction_lab.course_inventory ORDER BY course_id;
SELECT * FROM transaction_lab.enrollments ORDER BY id;
SELECT * FROM transaction_lab.payments ORDER BY id;
