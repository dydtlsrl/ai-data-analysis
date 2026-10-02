-- Chapter 09. transaction_lab 초기화
-- 목적: 01~09를 처음부터 다시 실습하고 싶을 때, transaction_lab 스키마만 제거합니다.
-- course_project(Chapter 07/08 데이터)는 절대 건드리지 않습니다.

SELECT current_database();
SELECT current_schema();

BEGIN;

DO $$
BEGIN
    IF current_database() <> 'ai_database_book' THEN
        RAISE EXCEPTION
            'transaction_lab 초기화 중단: 현재 데이터베이스는 %입니다. ai_database_book에 연결하세요.',
            current_database();
    END IF;
END
$$;

-- transaction_lab 스키마와 그 안의 모든 객체(테이블, 인덱스)를 함께 삭제합니다.
-- course_project 스키마는 이 DROP의 대상이 아니므로 영향을 받지 않습니다.
DROP SCHEMA IF EXISTS transaction_lab CASCADE;

-- 삭제 결과 확인
DO $$
BEGIN
    IF to_regnamespace('transaction_lab') IS NOT NULL THEN
        RAISE EXCEPTION 'transaction_lab 초기화 실패: 스키마가 아직 남아 있습니다.';
    END IF;

    IF (SELECT COUNT(*) FROM course_project.enrollments) <> 5 THEN
        RAISE EXCEPTION 'transaction_lab 초기화 중 course_project 데이터가 변경되었습니다. 즉시 확인하세요.';
    END IF;

    RAISE NOTICE 'Chapter 09 transaction_lab reset passed';
END
$$;

COMMIT;

-- 이후 01_transaction_lab_schema.sql부터 다시 실행하세요.
