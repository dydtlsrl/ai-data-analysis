<?php

require_once __DIR__ . '/config/db.php';

$instructorCount =
    $pdo->query("SELECT COUNT(*) FROM instructors")->fetchColumn();

$instructors = $pdo->query("
    SELECT
        instructor_id,
        name,
        email,
        department,
        created_at
    FROM instructors
    ORDER BY instructor_id DESC
    LIMIT 100
")->fetchAll();

$pageTitle = '강사 관리';
$activePage = 'instructors';

require __DIR__ . '/includes/header.php';
?>

<div class="summary-grid">

    <div class="stat-card">

        <div class="stat-label">
            전체 강사
        </div>

        <div class="stat-number">
            <?= number_format($instructorCount) ?>
        </div>

    </div>

</div>

<div class="card-box">

    <div class="card-head orange">
        강사 목록
    </div>

    <div class="table-wrap">

        <table class="admin-table">

            <thead>
            <tr>
                <th>ID</th>
                <th>이름</th>
                <th>Email</th>
                <th>소속</th>
                <th>등록일</th>
            </tr>
            </thead>

            <tbody>

            <?php foreach ($instructors as $row): ?>

                <tr>

                    <td>
                        <?= $row['instructor_id'] ?>
                    </td>

                    <td class="name-link">
                        <?= htmlspecialchars($row['name']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['email']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['department']) ?>
                    </td>

                    <td>
                        <?= htmlspecialchars($row['created_at']) ?>
                    </td>

                </tr>

            <?php endforeach; ?>

            </tbody>

        </table>

    </div>

</div>

<?php require __DIR__ . '/includes/footer.php'; ?>