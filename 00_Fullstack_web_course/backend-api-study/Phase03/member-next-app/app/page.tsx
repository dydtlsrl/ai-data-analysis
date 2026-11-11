// ============================================================
// app/page.tsx  (4강 버전)
// ------------------------------------------------------------
// [목적]  첫 화면(/)을 구성하는 주인(HomePage)
// [구조]  제목 영역 + MemberWorkspace 한 개
// [예상결과] 샘플 배열 없이도 MemberWorkspace가 FastAPI 데이터를 직접 조회해 보여준다
// ============================================================

// # 회원 작업 화면(검색·조회·등록 미리보기)을 가져온다
import MemberWorkspace from "../components/MemberWorkspace";

// # [컴포넌트] HomePage: 이 파일의 기본 내보내기 = "/" 주소에서 보이는 페이지
export default function HomePage() {
  return (
    <main>
      {/* # 수업 표시 문구 */}
      <p>Phase 03 · 04강 FastAPI 회원 목록 연동</p>
      <h1>회원 관리</h1>
      {/* # 3강과 달리 샘플 배열을 넘기지 않는다 */}
      <p>이제 샘플 배열 대신 FastAPI의 회원 데이터를 조회합니다.</p>

      {/* # props 없이 호출: 데이터는 MemberWorkspace가 스스로 가져온다 */}
      <MemberWorkspace />
    </main>
  );
}