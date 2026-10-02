-- Chapter 09. 05 두 번째 COMMIT과 좌석 부족(0행) 확인
-- 시작 상태: course 302 remaining_seats 1 (04는 ROLLBACK했으므로 302는 아직 차감되지 않음)
-- 완료 상태: 학생 103이 강의 302를 정상 확정(COMMIT) → remaining_seats 0
--            그 뒤 추가 신청 시도는 SQL 오류가 아니라 0행으로 끝나는 것을 확인
-- 04에서 ROLLBACK된 9002/9902는 커밋된 적이 없으므로 같은 번호를 다시 명시적으로 사용합니다.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

BEGIN;

-- 1) 학생 103의 강의 302 신청을 이번에는 끝까지 COMMIT합니다.
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
        9002, 103, course_id,
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

-- COMMIT 전 검증
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

    IF v_remaining_seats <> 0 OR v_enrollment_count <> 1 OR v_payment_count <> 1 THEN
        RAISE EXCEPTION
            '두 번째 COMMIT 검증 실패: remaining=%, enrollment=%, payment=%',
            v_remaining_seats, v_enrollment_count, v_payment_count;
    END IF;

    RAISE NOTICE 'Chapter 09 commit transaction (course 302, student 103) passed';
END
$$;

COMMIT;

-- 2) 좌석이 이미 0인 강의 302에 또 다른 학생이 신청을 시도하는 상황을 재현합니다.
--    조건부 UPDATE이므로 remaining_seats > 0 조건을 만족하는 행이 없어 0행이 반환됩니다.
--    이것은 PostgreSQL 문법 오류도 아니고 자동 ROLLBACK도 아닌, "정원 마감"이라는 정상적인 업무 결과입니다.
UPDATE transaction_lab.course_inventory
SET remaining_seats = remaining_seats - 1
WHERE course_id = 302
  AND remaining_seats > 0
RETURNING course_id, remaining_seats;
-- 실행 결과: 0 rows affected(문장 자체는 성공, 반환 행만 0개)가 보이면 정상입니다.

-- 3) 주 실습에서 명시적 ID(9001, 9002)를 직접 입력했으므로,
--    IDENTITY 시퀀스의 다음 값을 실제 사용한 마지막 번호 이후로 맞춰 둡니다.
--    이 ALTER는 이후 실습에서 별도로 새 신청을 자동 ID로 만들 때 번호가 겹치지 않게 하기 위한 정리입니다.
ALTER TABLE transaction_lab.enrollments
    ALTER COLUMN id RESTART WITH 9003;

ALTER TABLE transaction_lab.payments
    ALTER COLUMN id RESTART WITH 9903;

-- 최종 상태 확인
SELECT course_id, remaining_seats FROM transaction_lab.course_inventory ORDER BY course_id;
SELECT * FROM transaction_lab.enrollments ORDER BY id;
SELECT * FROM transaction_lab.payments ORDER BY id;
