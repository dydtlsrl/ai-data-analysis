<?php

$pageTitle = $pageTitle ?? 'Course Admin';
$activePage = $activePage ?? '';

?>

<!DOCTYPE html>
<html lang="ko">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title><?= htmlspecialchars($pageTitle) ?></title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <link
        rel="stylesheet"
        href="/assets/css/custom.css"
    >
</head>

<body>

<div class="main">

    <!-- 상단 가로 메뉴 -->
    <header class="topbar-horizontal">

        <div class="brand-horizontal">
            <span>★</span> 학생 관리 시스템
        </div>

        <nav class="top-menu">

            <a
                href="/index.php"
                class="<?= $activePage === 'dashboard' ? 'active' : '' ?>"
            >
                대시보드
            </a>

            <a
                href="/students.php"
                class="<?= $activePage === 'students' ? 'active' : '' ?>"
            >
                학생 관리
            </a>

            <a
                href="/instructors.php"
                class="<?= $activePage === 'instructors' ? 'active' : '' ?>"
            >
                강사 관리
            </a>

            <a
                href="/courses.php"
                class="<?= $activePage === 'courses' ? 'active' : '' ?>"
            >
                강좌 관리
            </a>

            <a
                href="/enrollments.php"
                class="<?= $activePage === 'enrollments' ? 'active' : '' ?>"
            >
                수강신청 관리
            </a>

        </nav>

        <div class="topbar-right">
            <span>학원관리자</span>
            <div class="avatar">관</div>
        </div>

    </header>

    

    <div class="content">