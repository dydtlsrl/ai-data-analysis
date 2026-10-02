<?php

require_once __DIR__ . '/config/db.php';

$enrollmentCount =
    $pdo->query("SELECT COUNT(*) FROM enrollments")->fetchColumn();

$status = $_GET['status'] ?? '';

$sql = "
    SELECT
        e.enrollment_id,
        s.name AS student_name,
        c.title AS course_title,
        i.name AS instructor_name,
        e.status,
        e.enrolled_at
    FROM enrollments e

    JOIN students s
        ON e.student_id = s.student_id

    JOIN courses c
        ON e.course_id = c.course_id

    JOIN instructors i
        ON c.instructor_id = i.instructor_id
";

if ($status !== '') {
    $sql .= " WHERE e.status = :status";
}

$sql .= "
    ORDER BY e.enrolled_at DESC
    LIMIT 100
";

$stmt = $pdo->prepare($sql);

if ($status !== '') {

    $stmt->execute([
        'status' => $status
    ]);

} else {

    $stmt->execute();
}

$enrollments = $stmt->fetchAll();

$pageTitle = '수강신청 관리';
$activePage = 'enrollments';

require __DIR__ . '/includes/header.php';
?>

<div class="summary-grid">

    <div class="stat-card">

        <div class="stat-label">
            전체 수강신청
        </div>

        <div class="stat-number">
            <?= number_format($enrollmentCount) ?>
        </div>

    </div>

</div>

<div class="card-box">

    <div class="card-head orange">
        최근 수강신청
    </div>

    <div class="p-3">

        <form method="GET">

            <select
                name="status"
                class="form-select"
                onchange="this.form.submit()"
            >

                <option value="">
                    전체 상태
                </option>

                <option
                    value="ENROLLED"
                    <?= $status === 'ENROLLED' ? 'selected' : '' ?>
                >
                    수강 중 (ENROLLED)
                </option>

                <option
                    value="COMPLETED"
                    <?= $status === 'COMPLETED' ? 'selected' : '' ?>
                >
                    수강 완료 (COMPLETED)
                </option>

                <option
                    value="CANCELLED"
                    <?= $status === 'CANCELLED' ? 'selected' : '' ?>
                >
                    취소 (CANCELLED)
                </option>

            </select>

        </form>

    </div>

    <div class="table-wrap">

        <table class="admin-table">

            <thead>
            <tr>
                <th>ID</th>
                <th>학생명</th>
                <th>강좌명</th>
                <th>강사명</th>
                <th>상태</th>
                <th>신청일</th>
            </tr>
            </thead>

            <tbody>

            <?php foreach ($enrollments as $row): ?>

                <?php
                $statusClass = match ($row['status']) {
                    'COMPLETED' => 'status-completed',
                    'CANCELLED' => 'status-cancelled',
                    default => 'status-enrolled'
                };
                ?>

                <tr>

                    <td>
                        <?= $row['enrollment_id'] ?>
                    </td>

                    <td class="name-link">
                        <?= htmlspecialchars($row['student_name']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['course_title']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['instructor_name']) ?>
                    </td>

                    <td>
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