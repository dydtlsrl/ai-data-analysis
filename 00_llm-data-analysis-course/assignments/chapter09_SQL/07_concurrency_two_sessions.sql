-- Chapter 09. 07 (선택 실습) Lock 대기 관찰 — 두 개의 SQL Editor(세션)가 필요합니다.
-- 목적: 잔여 좌석이 있는 강의(303, remaining_seats=1)에 두 연결이 동시에 접근할 때
--       READ COMMITTED 기본 격리 수준에서 Lock 대기가 어떻게 일어나는지 관찰합니다.
-- 이 파일 자체를 위에서 아래로 실행하지 않습니다. DBeaver에서 이 파일을 이용해
-- "세션 A" 창 하나, "세션 B" 창 하나를 각각 열고 아래 지시대로 번갈아 실행하세요.

SELECT current_database();
SELECT current_schema();
SHOW search_path;

-- PostgreSQL 기본 격리 수준을 먼저 확인합니다.
SHOW transaction_isolation;

-- ============================================================
-- 세션 A (첫 번째 DBeaver SQL Editor / 첫 번째 연결)에서 실행
-- ============================================================
-- BEGIN;
-- SELECT *
-- FROM transaction_lab.course_inventory
-- WHERE course_id = 303
-- FOR UPDATE;
--
-- 이 상태로 COMMIT/ROLLBACK을 하지 않고 잠시 대기합니다(세션 B로 이동).

-- ============================================================
-- 세션 B (두 번째 DBeaver SQL Editor / 두 번째 연결)에서 실행
-- ============================================================
-- BEGIN;
-- SET LOCAL lock_timeout = '5s';
-- SELECT *
-- FROM transaction_lab.course_inventory
-- WHERE course_id = 303
-- FOR UPDATE;
--
-- 관찰 포인트:
--   세션 A가 COMMIT/ROLLBACK 하기 전까지 세션 B는 대기합니다(일반적인 Lock 대기).
--   lock_timeout(5초)을 넘기면 세션 B에서 다음과 비슷한 오류가 발생할 수 있습니다.
--     ERROR:  canceling statement due to lock timeout
--   이 오류가 나면 세션 B에서 ROLLBACK으로 트랜잭션을 정리합니다.

-- ============================================================
-- 세션 A에서 이어서 실행 (세션 B가 대기 중인 상태에서)
-- ============================================================
-- COMMIT; -- 또는 ROLLBACK;
--
-- 세션 A가 종료되면, READ COMMITTED 기준으로 세션 B의 FOR UPDATE가
-- 최신 행을 잠그고 이어서 실행됩니다. 세션 B에서도 관찰이 끝나면 COMMIT 또는 ROLLBACK 합니다.
-- 이 선택 실습은 실제 좌석을 변경하지 않으므로, 세션 B는 관찰 후 ROLLBACK을 권장합니다.

-- ============================================================
-- Lock 대기와 Deadlock의 차이 (직접 재현하지 않고 개념만 정리)
-- ============================================================
-- 일반 Lock 대기: 한 트랜잭션이 다른 트랜잭션의 잠금 해제를 기다림 (위 예제)
-- Deadlock: 두 트랜잭션이 서로가 가진 잠금을 순환 구조로 기다림
--   트랜잭션 A: course 301 잠금 → course 302 대기
--   트랜잭션 B: course 302 잠금 → course 301 대기
-- PostgreSQL은 Deadlock을 감지하면 한 트랜잭션을 오류로 강제 종료합니다.
-- 이 파일에서는 실제 Deadlock을 유발하는 SQL을 포함하지 않습니다(개념 학습 목적).
