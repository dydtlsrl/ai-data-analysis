// ============================================================
// app/members/page.tsx  (6강: 새 파일)
// ------------------------------------------------------------
// [목적]  "/members" 주소의 회원 목록 페이지 (진열대 방)
// [구조]  제목 영역 + 메인 화면 링크 + MemberWorkspace(검색·CRUD 그대로)
// [예상결과] http://localhost:3000/members 에서 5강의 목록·검색·등록·수정·삭제가 그대로 보인다
// ============================================================

// # Link: 전체 페이지를 새로고침하지 않고 Next.js 방식으로 이동시키는 링크 도구
import Link from "next/link";
// # 5강에서 완성한 회원 작업 화면을 그대로 가져다 쓴다 (코드를 복사하지 않고 재사용)
import MemberWorkspace from "../../components/MemberWorkspace";

// # [컴포넌트] MembersPage: 이 파일의 기본 내보내기 = "/members" 주소에서 보이는 페이지
export default function MembersPage() {
  return (
    <main
      style={{
        maxWidth: 880,
        margin: "48px auto",
        padding: "0 24px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* # 수업 표시 문구와 제목 */}
      <p style={{ color: "#2563eb", fontWeight: 700 }}>
        Phase 03 · 06강 회원 목록과 상세 이동
      </p>
      <h1 style={{ fontSize: 36, color: "#0f172a" }}>회원관리 시스템</h1>
      <p>회원 카드의 상세 보기를 눌러 회원 상세 페이지로 이동합니다.</p>

      {/* # 첫 화면("/")으로 돌아가는 링크 */}
      <p>
        <Link href="/">기존 메인 화면으로</Link>
      </p>

      {/* # 5강 코드 그대로: 검색 + 목록 + 등록·수정·삭제 */}
      <MemberWorkspace />
    </main>
  );
}