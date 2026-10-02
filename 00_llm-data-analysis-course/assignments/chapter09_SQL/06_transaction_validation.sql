-- Chapter 09. 06 최종 정합성 검증
-- 목적: 01~05를 순서대로 실행한 뒤, 좌석·신청·결제 세 테이블이
--       서로 모순되지 않는 상태인지 자동으로 확인하는 완료 게이트입니다.
-- 이 파일은 조회 전용이며 데이터를 변경하지 않습니다.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

DO $$
DECLARE
    v_course_project_enrollments bigint;
    v_lab_enrollments bigint;
    v_lab_payments bigint;
    v_remaining_301 int;
    v_remaining_302 int;
    v_remaining_303 int;
    v_seat_range_violation bigint;
    v_progress_without_payment bigint;
    v_amount_mismatch bigint;
    v_orphan_payment bigint;
    v_duplicate_active bigint;
    v_active_enrollment_count bigint;
    v_seats_used bigint;
BEGIN
    -- 1) Chapter 07 데이터가 그대로인지 (transaction_lab 실습이 건드리지 않았는지) 확인
    SELECT COUNT(*) INTO v_course_project_enrollments FROM course_project.enrollments;

    -- 2) 실습 결과 행 수
    SELECT COUNT(*) INTO v_lab_enrollments FROM transaction_lab.enrollments;
    SELECT COUNT(*) INTO v_lab_payments FROM transaction_lab.payments;

    -- 3) 강의별 잔여 좌석
    SELECT remaining_seats INTO v_remaining_301 FROM transaction_lab.course_inventory WHERE course_id = 301;
    SELECT remaining_seats INTO v_remaining_302 FROM transaction_lab.course_inventory WHERE course_id = 302;
    SELECT remaining_seats INTO v_remaining_303 FROM transaction_lab.course_inventory WHERE course_id = 303;

    -- 4) 좌석 범위 위반: remaining_seats가 0 미만이거나 capacity를 초과하는 행
    --    (CHECK 제약이 있어 이론상 0이어야 하지만, 업무 규칙 관점에서 다시 한번 확인)
    SELECT COUNT(*) INTO v_seat_range_violation
    FROM transaction_lab.course_inventory
    WHERE remaining_seats < 0 OR remaining_seats > capacity;

    -- 5) '수강중' 신청인데 연결된 결제가 없는 경우
    SELECT COUNT(*) INTO v_progress_without_payment
    FROM transaction_lab.enrollments AS e
    WHERE e.status = '수강중'
      AND NOT EXISTS (
          SELECT 1 FROM transaction_lab.payments AS p
          WHERE p.enrollment_id = e.id
      );

    -- 6) 신청 recorded_amount와 결제 amount가 다른 경우
    SELECT COUNT(*) INTO v_amount_mismatch
    FROM transaction_lab.enrollments AS e
    JOIN transaction_lab.payments AS p
        ON p.enrollment_id = e.id
    WHERE e.recorded_amount <> p.amount;

    -- 7) 존재하지 않는 enrollment를 참조하는 결제 (FK가 있어 이론상 발생 불가, 방어적으로 확인)
    SELECT COUNT(*) INTO v_orphan_payment
    FROM transaction_lab.payments AS p
    WHERE NOT EXISTS (
        SELECT 1 FROM transaction_lab.enrollments AS e WHERE e.id = p.enrollment_id
    );

    -- 8) 같은 학생·강의의 중복 활성('수강중') 신청 (부분 고유 인덱스가 있어 이론상 발생 불가)
    SELECT COUNT(*) INTO v_duplicate_active
    FROM (
        SELECT student_id, course_id
        FROM transaction_lab.enrollments
        WHERE status = '수강중'
        GROUP BY student_id, course_id
        HAVING COUNT(*) > 1
    ) AS duplicated;

    -- 9) 활성 신청 수와 사용 좌석 수(capacity - remaining_seats 합)가 같은지 확인
    SELECT COUNT(*) INTO v_active_enrollment_count
    FROM transaction_lab.enrollments
    WHERE status = '수강중';

    SELECT COALESCE(SUM(capacity - remaining_seats), 0) INTO v_seats_used
    FROM transaction_lab.course_inventory;

    IF v_course_project_enrollments <> 5
       OR v_lab_enrollments <> 2
       OR v_lab_payments <> 2
       OR v_remaining_301 <> 1
       OR v_remaining_302 <> 0
       OR v_remaining_303 <> 1
       OR v_seat_range_violation <> 0
       OR v_progress_without_payment <> 0
       OR v_amount_mismatch <> 0
       OR v_orphan_payment <> 0
       OR v_duplicate_active <> 0
       OR v_active_enrollment_count <> v_seats_used THEN
        RAISE EXCEPTION
            'Chapter 09 검증 실패: course_project=%, lab_enrollments=%, lab_payments=%, remaining(301/302/303)=%/%/%, seat_violation=%, progress_no_payment=%, amount_mismatch=%, orphan_payment=%, duplicate_active=%, active=%, seats_used=%',
            v_course_project_enrollments, v_lab_enrollments, v_lab_payments,
            v_remaining_301, v_remaining_302, v_remaining_303,
            v_seat_range_violation, v_progress_without_payment, v_amount_mismatch,
            v_orphan_payment, v_duplicate_active,
            v_active_enrollment_count, v_seats_used;
    END IF;

    RAISE NOTICE 'Chapter 09 main transaction validation passed';
END
$$;

-- 사람이 눈으로 다시 확인할 최종 요약
SELECT
    ci.course_id,
    c.title,
    ci.capacity,
    ci.remaining_seats
FROM transaction_lab.course_inventory AS ci
JOIN course_project.courses AS c
    ON c.id = ci.course_id
ORDER BY ci.course_id;

SELECT
    e.id AS enrollment_id,
    e.student_id,
    e.course_id,
    e.status,
    e.recorded_amount,
    p.id AS payment_id,
    p.amount AS payment_amount
FROM transaction_lab.enrollments AS e
LEFT JOIN transaction_lab.payments AS p
    ON p.enrollment_id = e.id
ORDER BY e.id;
