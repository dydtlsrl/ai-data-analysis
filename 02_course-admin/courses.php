<?php

require_once __DIR__ . '/config/db.php';

$courseCount =
    $pdo->query("SELECT COUNT(*) FROM courses")->fetchColumn();

$courses = $pdo->query("
    SELECT
        c.course_id,
        c.title,
        c.category,
        c.capacity,
        i.name AS instructor_name
    FROM courses c
    JOIN instructors i
        ON c.instructor_id = i.instructor_id
    ORDER BY c.course_id DESC
")->fetchAll();

$pageTitle = '강좌 관리';
$activePage = 'courses';

require __DIR__ . '/includes/header.php';
?>

<div class="summary-grid">

    <div class="stat-card">

        <div class="stat-label">
            전체 강좌
        </div>

        <div class="stat-number">
            <?= number_format($courseCount) ?>
        </div>

    </div>

</div>

<div class="card-box">

    <div class="card-head orange">
        강좌 목록
    </div>

    <div class="table-wrap">

        <table class="admin-table">

            <thead>
            <tr>
                <th>ID</th>
                <th>강좌명</th>
                <th>강사명</th>
                <th>카테고리</th>
                <th>정원</th>
            </tr>
            </thead>

            <tbody>

            <?php foreach ($courses as $row): ?>

                <tr>

                    <td>
                        <?= $row['course_id'] ?>
                    </td>

                    <td class="name-link">
                        <?= htmlspecialchars($row['title']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['instructor_name']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['category']) ?>
                    </td>

                    <td>
                        <?= number_format($row['capacity']) ?>
                    </td>

                </tr>

            <?php endforeach; ?>

            </tbody>

        </table>

    </div>

</div>

<?php require __DIR__ . '/includes/footer.php'; ?>