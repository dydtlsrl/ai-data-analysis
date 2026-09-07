-- ============================================
-- AX 2회차 SQL & Database 과제
-- ============================================


-- Part 1. Schema와 Table 만들기

CREATE SCHEMA IF NOT EXISTS practice;

CREATE TABLE practice.members (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INTEGER,
    joined_at DATE
);


-- Part 2. 회원 데이터 입력

INSERT INTO practice.members
(name, email, age, joined_at)
VALUES
('김민수', 'minsu@example.com', 25, '2026-08-01'),
('이서연', 'seoyeon@example.com', 31, '2026-08-03'),
('박준호', 'junho@example.com', 22, '2026-08-05'),
('최지우', 'jiwoo@example.com', 28, '2026-08-10'),
('정하늘', 'haneul@example.com', 24, '2026-08-15');


-- 전체 회원 조회
SELECT * FROM practice.members;


-- 이름과 이메일만 조회
SELECT name, email
FROM practice.members;


-- 25세 이상 회원 조회
SELECT *
FROM practice.members
WHERE age >= 25;


-- 특정 이름의 회원 조회
SELECT *
FROM practice.members
WHERE name = '김민수';


-- 나이가 많은 순서로 조회
SELECT *
FROM practice.members
ORDER BY age DESC;


-- 가입일 순서로 조회
SELECT *
FROM practice.members
ORDER BY joined_at ASC;


-- Part 3. UPDATE

UPDATE practice.members
SET age = 30
WHERE member_id = 1;


-- 수정 결과 확인
SELECT *
FROM practice.members
WHERE member_id = 1;


-- DELETE

DELETE FROM practice.members
WHERE member_id = 5;


-- 삭제 결과 확인
SELECT *
FROM practice.members;


-- Part 4. 집계 함수

-- 전체 회원 수
SELECT COUNT(*) AS total_members
FROM practice.members;


-- 회원 평균 나이
SELECT AVG(age) AS average_age
FROM practice.members;


-- 가장 나이가 많은 회원의 나이
SELECT MAX(age) AS max_age
FROM practice.members;


-- 가장 나이가 어린 회원의 나이
SELECT MIN(age) AS min_age
FROM practice.members;


-- 25세 이상 회원 수
SELECT COUNT(*) AS members_over_25
FROM practice.members
WHERE age >= 25;


-- ============================================
-- 도전 문제
-- ============================================

-- 가장 최근에 가입한 회원
SELECT *
FROM practice.members
ORDER BY joined_at DESC
LIMIT 1;


-- 평균 나이보다 나이가 많은 회원
SELECT *
FROM practice.members
WHERE age > (
    SELECT AVG(age)
    FROM practice.members
);


-- 조건 2개 이상 사용
SELECT *
FROM practice.members
WHERE age >= 25
AND joined_at >= '2026-08-01'
ORDER BY age DESC;