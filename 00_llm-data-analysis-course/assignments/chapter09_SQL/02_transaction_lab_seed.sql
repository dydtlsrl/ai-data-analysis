-- Chapter 09. 02 transaction_lab 좌석 초기 데이터 입력
-- 시작 상태: transaction_lab 세 테이블 모두 0행
-- 완료 상태: course_inventory 3행 (강의 301/302/303), enrollments/payments는 여전히 0행
-- 좌석 입력과 검증을 하나의 트랜잭션으로 실행합니다.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

BEGIN;

-- 사전 조건: 스키마·테이블이 있고, 아직 좌석이 입력되지 않았는지 확인합니다.
DO $$
DECLARE
    v_inventory_count bigint;
BEGIN
    IF to_regclass('transaction_lab.course_inventory') IS NULL THEN
        RAISE EXCEPTION '좌석 입력 중단: 01_transaction_lab_schema.sql을 먼저 실행하세요.';
    END IF;

    SELECT COUNT(*) INTO v_inventory_count FROM transaction_lab.course_inventory;

    IF v_inventory_count <> 0 THEN
        RAISE EXCEPTION '좌석 입력 중단: course_inventory가 이미 %행 있습니다.', v_inventory_count;
    END IF;
END
$$;

-- 강의 301(데이터베이스 입문) capacity 2, 강의 302(정규화 실습)·303(파이썬 데이터 분석) capacity 1.
-- capacity/remaining_seats는 course_project.courses와 무관한 이 실습만의 좌석 값입니다.
INSERT INTO transaction_lab.course_inventory (course_id, capacity, remaining_seats)
VALUES
    (301, 2, 2),
    (302, 1, 1),
    (303, 1, 1);

-- 입력 결과 검증: 3행, 강의별 capacity=remaining_seats(아직 신청 전이므로 전부 가득 참).
DO $$
DECLARE
    v_row_count bigint;
    v_301_remaining int;
    v_302_remaining int;
    v_303_remaining int;
BEGIN
    SELECT COUNT(*) INTO v_row_count FROM transaction_lab.course_inventory;

    SELECT remaining_seats INTO v_301_remaining
    FROM transaction_lab.course_inventory WHERE course_id = 301;
    SELECT remaining_seats INTO v_302_remaining
    FROM transaction_lab.course_inventory WHERE course_id = 302;
    SELECT remaining_seats INTO v_303_remaining
    FROM transaction_lab.course_inventory WHERE course_id = 303;

    IF v_row_count <> 3
       OR v_301_remaining <> 2
       OR v_302_remaining <> 1
       OR v_303_remaining <> 1 THEN
        RAISE EXCEPTION
            '좌석 입력 검증 실패: rows=%, 301=%, 302=%, 303=%',
            v_row_count, v_301_remaining, v_302_remaining, v_303_remaining;
    END IF;

    RAISE NOTICE 'Chapter 09 transaction_lab seed passed';
END
$$;

COMMIT;

-- 입력 결과 확인
SELECT
    ci.course_id,
    c.title,
    c.price,
    ci.capacity,
    ci.remaining_seats
FROM transaction_lab.course_inventory AS ci
JOIN course_project.courses AS c
    ON c.id = ci.course_id
ORDER BY ci.course_id;
