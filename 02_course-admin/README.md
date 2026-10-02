# 수강 관리 PHP/MySQL 실습

원본: [sangjae-lee97/course-admin](https://github.com/sangjae-lee97/course-admin), 커밋 `a96a7548169c74d5367d3f1e345dffc516da0a71`.

학생 등록, 학생·강사·강좌·수강신청 조회와 수강 상태 필터를 실습하는 앱입니다. 현재 레포의 Python·PostgreSQL 실습과 별도로 PHP 및 MySQL을 사용합니다.

## 실행 조건

PHP와 `pdo_mysql` 확장, MySQL, 앱에 맞는 `course_system` 데이터베이스가 필요합니다. 원본에는 스키마 생성 SQL이나 시드 데이터가 없습니다. `majors`, `students`, `instructors`, `courses`, `enrollments` 테이블과 PHP 조회문에서 사용하는 컬럼을 먼저 준비해야 합니다. 기존 수업의 PostgreSQL SQL을 그대로 MySQL에 실행할 수는 없습니다.

DB 설정은 `config/db.php`에서 다음 환경변수를 읽습니다. 원본에 있던 하드코딩 비밀번호는 제거했습니다.

| 환경변수 | 기본값 |
| --- | --- |
| `COURSE_DB_HOST` | `localhost` |
| `COURSE_DB_PORT` | `3306` |
| `COURSE_DB_NAME` | `course_system` |
| `COURSE_DB_USER` | `root` |
| `COURSE_DB_PASSWORD` | 빈 문자열 |

PowerShell에서 DB 설정을 지정한 뒤, 레포 루트에서 앱 폴더를 웹 루트로 실행합니다.

```powershell
$env:COURSE_DB_HOST = 'localhost'
$env:COURSE_DB_PORT = '3306'
$env:COURSE_DB_NAME = 'course_system'
$env:COURSE_DB_USER = 'your_mysql_user'
$env:COURSE_DB_PASSWORD = 'your_mysql_password'
php -S localhost:8000 -t 02_course-admin
```

[http://localhost:8000](http://localhost:8000)에서 앱을 확인합니다. CSS·JS·메뉴 링크는 이 실행 방식에 맞춰 `/course-admin/` 접두사를 제거했습니다. 현재 환경에서는 PHP 실행기가 없어 실제 실행·DB 연결은 확인하지 않았습니다.
