<?php

require_once __DIR__ . '/config/db.php';

$errorMessage = '';

$majors = $pdo->query("
    SELECT major_id, major_name
    FROM majors
    ORDER BY major_name
")->fetchAll();

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $majorId = $_POST['major_id'] ?? '';

    if ($name === '' || $email === '') {

        $errorMessage = '이름과 이메일은 필수입니다.';

    } else {

        try {

            $sql = "
                INSERT INTO students
                    (name, email, major_id)
                VALUES
                    (:name, :email, :major_id)
            ";

            $stmt = $pdo->prepare($sql);

            $stmt->execute([
                'name' => $name,
                'email' => $email,
                'major_id' => $majorId ?: null
            ]);

            header('Location: students.php?success=1');
            exit;

        } catch (PDOException $e) {

            $errorMessage =
                '학생 등록에 실패했습니다. 이메일 중복 여부를 확인해주세요.';
        }
    }
}

$studentCount =
    $pdo->query("SELECT COUNT(*) FROM students")->fetchColumn();

$majorCount =
    $pdo->query("SELECT COUNT(*) FROM majors")->fetchColumn();

$students = $pdo->query("
    SELECT
        s.student_id,
        s.name,
        s.email,
        m.major_name,
        s.created_at
    FROM students s
    LEFT JOIN majors m
        ON s.major_id = m.major_id
    ORDER BY s.student_id DESC
    LIMIT 50
")->fetchAll();

$pageTitle = '학생 관리';
$activePage = 'students';

require __DIR__ . '/includes/header.php';
?>

<?php if (isset($_GET['success'])): ?>

    <div class="alert alert-success">
        학생 등록이 완료되었습니다.
    </div>

<?php endif; ?>

<?php if ($errorMessage !== ''): ?>

    <div class="alert alert-danger">
        <?= htmlspecialchars($errorMessage) ?>
    </div>

<?php endif; ?>

<div class="summary-grid">

    <div class="stat-card">
        <div class="stat-label">전체 학생</div>
        <div class="stat-number">
            <?= number_format($studentCount) ?>
        </div>
    </div>

    <div class="stat-card">
        <div class="stat-label">전공 종류</div>
        <div class="stat-number">
            <?= number_format($majorCount) ?>
        </div>
    </div>

</div>

<div class="content-grid">

    <div class="card-box">

    <div class="card-head">
        학생 등록
    </div>

    <div class="card-body">

        <form method="POST">

            <div class="mb-3">
                <label class="form-label">이름</label>

                <input
                    type="text"
                    name="name"
                    class="form-control"
                    required
                >
            </div>

            <div class="mb-3">
                <label class="form-label">이메일</label>

                <input
                    type="email"
                    name="email"
                    class="form-control"
                    required
                >
            </div>

            <div class="mb-3">

                <label class="form-label">전공</label>

                <select
                    name="major_id"
                    class="form-select"
                >

                    <option value="">
                        전공 선택
                    </option>

                    <?php foreach ($majors as $major): ?>

                        <option
                            value="<?= $major['major_id'] ?>"
                        >
                            <?= htmlspecialchars($major['major_name']) ?>
                        </option>

                    <?php endforeach; ?>

                </select>

            </div>

            <button
                class="btn btn-dark-admin w-100"
                type="submit"
            >
                학생 등록
            </button>

            

        </form>

    </div>

</div>

    <div class="card-box">

        <div class="card-head orange">
            학생 목록
        </div>
        <div class="p-3 d-flex gap-2">

        <input
            type="text"
            id="keyword"
            class="form-control"
            placeholder="학생 이름 또는 이메일 검색"
        >

        <button
            type="button"
            id="searchButton"
            class="btn btn-secondary"
        >
            검색
        </button>

        </div>

        <div class="table-wrap">

            <table class="admin-table">

                <thead>
                <tr>
                    <th>ID</th>
                    <th>이름</th>
                    <th>Email</th>
                    <th>전공</th>
                    <th>등록일</th>
                </tr>
                </thead>

                <tbody>

                <?php foreach ($students as $student): ?>

                    <tr>

                        <td>
                            <?= $student['student_id'] ?>
                        </td>

                        <td class="name-link">
                            <?= htmlspecialchars($student['name']) ?>
                        </td>

                        <td>
                            <?= htmlspecialchars($student['email']) ?>
                        </td>

                        <td>

                            <?php if ($student['major_name']): ?>

                                <span class="major-badge">
                                    <?= htmlspecialchars($student['major_name']) ?>
                                </span>

                            <?php else: ?>

                                -

                            <?php endif; ?>

                        </td>

                        <td>
                            <?= htmlspecialchars($student['created_at']) ?>
                        </td>

                    </tr>

                <?php endforeach; ?>

                </tbody>

            </table>

        </div>

    </div>

</div>

<?php require __DIR__ . '/includes/footer.php'; ?>