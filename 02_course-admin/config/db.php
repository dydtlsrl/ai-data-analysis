<?php

$host = getenv('COURSE_DB_HOST') ?: 'localhost';
$port = getenv('COURSE_DB_PORT') ?: '3306';
$dbname = getenv('COURSE_DB_NAME') ?: 'course_system';
$username = getenv('COURSE_DB_USER') ?: 'root';
$password = getenv('COURSE_DB_PASSWORD') ?: '';

$dsn = "mysql:host={$host};port={$port};dbname={$dbname};charset=utf8mb4";

$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES => false,
];

try {
    $pdo = new PDO($dsn, $username, $password, $options);
} catch (PDOException $e) {
    exit('DB 연결 실패: ' . $e->getMessage());
}