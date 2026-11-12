// ============================================================
// app/members/[memberId]/page.tsx  (6강: Suspense 적용 버전)
// ------------------------------------------------------------
// [목적]  "/members/2" 같은 주소의 상세 페이지 틀 (손님 전용 방)
// [구조]  바깥 틀(main) + Suspense(준비 중 팻말) + MemberDetail
// [예상결과] 빌드가 통과하고, 상세 화면은 "불러오는 중" 팻말 뒤에 회원 정보로 채워진다
// ============================================================

// # Suspense: "이 안의 내용이 준비될 때까지 대신 보여 줄 팻말(fallback)"을 거는 도구
import { Suspense } from "react";
// # 폴더 한 단계 더 안쪽이라 "../" 가 3번이다 (app/members/[memberId] → components)
import MemberDetail from "../../../components/MemberDetail";

// # [컴포넌트] MemberDetailPage: 바깥 틀 + Suspense + 안쪽 내용
export default function MemberDetailPage() {
  return (
    <main
      style={{
        maxWidth: 880,
        margin: "48px auto",
        padding: "0 24px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* # useParams는 주소 값(실행 중에만 알 수 있음)을 읽으므로 Suspense로 감싸야 한다 */}
      {/* # fallback: 주소 값이 준비되기 전에 먼저 보이는 팻말 */}
      <Suspense fallback={<p role="status">회원 정보를 준비하는 중입니다...</p>}>
        <MemberDetail />
      </Suspense>
    </main>
  );
}