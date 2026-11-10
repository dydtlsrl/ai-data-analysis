// ==================================================================
// # 파일: app/page.tsx  (02강 버전)
// # 역할: 가게 주인. 재료(샘플 회원 3명)를 준비해서 점원(MemberList)에게 건네준다.
// # 전체 흐름: 접속(/) → HomePage 실행 → 재료 준비 → MemberList에 전달 → 카드 3장 화면 표시
// ==================================================================

// # [명령어] import MemberList from "../components/MemberList";
// # 구조: "../"는 한 칸 위(프로젝트 루트)로 올라가서 components 폴더의 MemberList를 가져온다.
// # 목적: STEP 04에서 만든 점원을 이 파일에서 부르려고 가져온다.
import MemberList from "../components/MemberList";

// # [명령어] import type { Member } from "../types/member";
// # 목적: 주문서 양식(Member)을 가져와서, 아래 샘플 데이터가 양식에 맞는지 검사하게 한다.
import type { Member } from "../types/member";

// # [명령어] const sampleMembers: Member[] = [ ... ];
// # 구조: "const sampleMembers"는 이름표를 붙인 상자를 만든다.
// #       ": Member[]"는 "이 상자에는 Member 양식을 따르는 회원이 여러 명 들어간다"는 약속이다.
// #       [ ... ] 안에 회원을 { } 로 하나씩 적고, 쉼표로 구분한다.
// # 목적: 서버(FastAPI)가 없으니 화면 연습용 가짜 회원 3명을 직접 적어 둔다. (4강에서 진짜 데이터로 바꾼다)
// # 예상결과: 아직 화면에는 안 보인다. 아래에서 점원에게 건네줘야 보인다.
const sampleMembers: Member[] = [
  // # 회원 한 명 = { 칸이름: 값, ... }. Member 양식의 칸 4개를 모두 채워야 한다.
  {
    member_id: 1,
    name: "Kim",
    email: "kim@example.com",
    age: 30,
  },
  {
    member_id: 2,
    name: "Lee",
    email: "lee@example.com",
    age: 27,
  },
  {
    member_id: 3,
    name: "Park",
    email: "park@example.com",
    age: 35,
  },
];

// # [명령어] export default function HomePage() { ... }
// # 목적: Next.js가 "/" 주소의 화면으로 사용하는 대표 함수다. (1강과 같은 역할)
export default function HomePage() {
  return (
    // # [태그] <main style={{ ... }}>
    // # 구조: 페이지 전체를 감싸는 큰 상자다. 가운데에 880px 폭으로 모으는 스타일이다.
    // # 예상결과: 내용이 화면 가운데에 모여 보인다.
    <main
      style={{
        maxWidth: 880,
        margin: "48px auto",
        padding: "0 24px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      {/* # [태그] <p> : 맨 위 파란 글씨 */}
      {/* # 예상결과: "Phase 03 · 02강 React Component와 TypeScript"가 파란 굵은 글씨로 보인다. */}
      <p style={{ color: "#2563eb", fontWeight: 700 }}>
        Phase 03 · 02강 React Component와 TypeScript
      </p>

      {/* # [태그] <h1> : 큰 제목 */}
      {/* # 예상결과: "회원관리 시스템" (다크 모드에서는 색이 어두워 잘 안 보일 수 있음) */}
      <h1 style={{ fontSize: 36, color: "#0f172a" }}>
        회원관리 시스템
      </h1>

      {/* # [태그] <p> : 설명 문장 */}
      {/* # 예상결과: 회원 목록을 작은 Component로 나눈다는 설명이 두 줄로 보인다. */}
      <p style={{ color: "#475569", lineHeight: 1.7 }}>
        회원 목록을 작은 Component로 나누어 보여줍니다.
        현재는 샘플 데이터이며, 실제 API 연결은 4강입니다.
      </p>

      {/* # [핵심] <MemberList members={sampleMembers} /> */}
      {/* # 구조: 우리가 만든 MemberList를 HTML 태그처럼 부른다. */}
      {/* #       "members={sampleMembers}"는 "members라는 이름으로 준비한 재료 상자(sampleMembers)를 건네준다"는 뜻이다. (Props 전달) */}
      {/* #       { } 안은 글자가 아니라 변수(상자)라서 따옴표 대신 중괄호를 쓴다. */}
      {/* # 목적: 이 한 줄이 점원을 부르는 순간이다. 여기서부터 MemberList → MemberCard로 이어진다. */}
      {/* # 예상결과: "회원 목록 (3명)"과 Kim, Lee, Park 카드 3장이 나타난다. */}
      <MemberList members={sampleMembers} />

      {/* # [태그] <p> : 맨 아래 다음 강의 안내 */}
      {/* # 예상결과: "다음 단계: 03강 · 검색과 입력 Form" */}
      <p style={{ color: "#64748b", marginTop: 32 }}>
        다음 단계: 03강 · 검색과 입력 Form
      </p>
    </main>
  );
}