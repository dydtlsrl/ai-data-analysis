<?php

require_once __DIR__ . '/config/db.php';

$studentCount =
    $pdo->query("SELECT COUNT(*) FROM students")->fetchColumn();

$instructorCount =
    $pdo->query("SELECT COUNT(*) FROM instructors")->fetchColumn();

$courseCount =
    $pdo->query("SELECT COUNT(*) FROM courses")->fetchColumn();

$enrollmentCount =
    $pdo->query("SELECT COUNT(*) FROM enrollments")->fetchColumn();

$sql = "
    SELECT
        e.enrollment_id,
        s.name AS student_name,
        c.title AS course_title,
        e.status,
        e.enrolled_at
    FROM enrollments e
    JOIN students s
        ON e.student_id = s.student_id
    JOIN courses c
        ON e.course_id = c.course_id
    ORDER BY e.enrolled_at DESC
    LIMIT 10
";

$recentEnrollments = $pdo->query($sql)->fetchAll();

$pageTitle = '대시보드';
$activePage = 'dashboard';

require __DIR__ . '/includes/header.php';
?>

<div class="summary-grid">

    <div class="stat-card">
        <div class="stat-label">전체 학생</div>
        <div class="stat-number">
            <?= number_format($studentCount) ?>
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-label">전체 강사</div>
        <div class="stat-number">
            <?= number_format($instructorCount) ?>
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-label">전체 강좌</div>
        <div class="stat-number">
            <?= number_format($courseCount) ?>
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-label">전체 수강신청</div>
        <div class="stat-number">
            <?= number_format($enrollmentCount) ?>
        </div>
    </div>

</div>

<div class="card-box">

    <div class="card-head orange">
        최근 수강신청 10건
    </div>

    <div class="table-wrap">

        <table class="admin-table">

            <thead>
            <tr>
                <th>ID</th>
                <th>학생</th>
                <th>강좌</th>
                <th>상태</th>
                <th>신청일</th>
            </tr>
            </thead>

            <tbody>

            <?php foreach ($recentEnrollments as $row): ?>

                <tr>

                    <td>
                        <?= htmlspecialchars($row['enrollment_id']) ?>
                    </td>

                    <td class="name-link">
                        <?= htmlspecialchars($row['student_name']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['course_title']) ?>
                    </td>

                    <td>

                        <?php
                        $statusClass = match ($row['status']) {
                            'COMPLETED' => 'status-completed',
                            'CANCELLED' => 'status-cancelled',
                            default => 'status-enrolled'
                        };
                        ?>

                        <span class="status <?= $statusClass ?>">
                            <?= htmlspecialchars($row['status']) ?>
                        </span>

                    </td>

                    <td>
                        <?= htmlspecialchars($row['enrolled_at']) ?>
                    </td>

                </tr>

            <?php endforeach; ?>

            </tbody>

        </table>

    </div>

</div>

<?php require __DIR__ . '/includes/footer.php'; ?>