// ==================================================================
// # 파일: app/page.tsx  (03강 버전)
// # 역할: 가게 주인. 재료(샘플 회원 3명)를 준비해서 MemberWorkspace(손님 영역)에 건네준다.
// # 이 파일은 "use client"가 없다 → Server Component(주방). 보여주고 건네주기만 한다.
// # 전체 흐름: 주인(page) → MemberWorkspace(검색·폼) → MemberList(점원) → MemberCard(틀)
// ==================================================================

// # [명령어] import MemberWorkspace from "../components/MemberWorkspace";
// # 구조: "../"는 한 칸 위(프로젝트 루트)로 올라가 components 폴더의 MemberWorkspace를 가져온다.
// # 목적: 방금 STEP 02에서 만든 손님 영역을 이 파일에서 부르려고 가져온다.
import MemberWorkspace from "../components/MemberWorkspace";

// # [명령어] import type { Member } from "../types/member";
// # 목적: 주문서 양식(Member)을 가져와서, 아래 샘플 데이터가 양식에 맞는지 검사하게 한다.
import type { Member } from "../types/member";

// # [명령어] const sampleMembers: Member[] = [ ... ];
// # 구조: 2강과 같다. "Member 양식을 따르는 회원 여러 명"을 담은 상자다.
// #       한 줄에 한 명씩 { 칸이름: 값, ... }으로 적는다. (2강보다 코드가 짧아졌을 뿐 내용은 같다)
// # 목적: 서버(FastAPI)가 없으니 연습용 가짜 회원 3명을 직접 적어 둔다. (4강에서 진짜 데이터로 바꾼다)
// # 예상결과: 아직 화면에는 안 보인다. 아래에서 MemberWorkspace에 건네줘야 보인다.
const sampleMembers: Member[] = [
  { member_id: 1, name: "Kim", email: "kim@example.com", age: 30 },
  { member_id: 2, name: "Lee", email: "lee@example.com", age: 27 },
  { member_id: 3, name: "Park", email: "park@example.com", age: 35 },
];

// # [명령어] export default function HomePage() { ... }
// # 목적: Next.js가 "/" 주소의 화면으로 사용하는 대표 함수다. (1~2강과 같은 역할)
export default function HomePage() {
  return (
    // # [태그] <main style={{ ... }}>
    // # 구조: 페이지 전체를 감싸는 큰 상자. 가운데에 880px 폭으로 모으는 스타일이다.
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
      {/* # 예상결과: "Phase 03 · 03강 Props · State · Event"가 파란 굵은 글씨로 보인다. */}
      <p style={{ color: "#2563eb", fontWeight: 700 }}>
        Phase 03 · 03강 Props · State · Event
      </p>

      {/* # [태그] <h1> : 큰 제목 */}
      {/* # 예상결과: "회원관리 시스템" (다크 모드에서는 색이 어두워 잘 안 보일 수 있음. 코드 오류 아님) */}
      <h1 style={{ fontSize: 36, color: "#0f172a" }}>회원관리 시스템</h1>

      {/* # [태그] <p> : 설명 문장 */}
      {/* # 예상결과: 검색과 입력 폼을 실습한다는 설명, API는 4강·저장은 5강이라는 안내 */}
      <p style={{ color: "#475569" }}>
        React State로 회원 검색과 입력 폼을 실습합니다.
        실제 API 조회는 4강, DB 저장은 5강에서 진행합니다.
      </p>

      {/* # [핵심] <MemberWorkspace initialMembers={sampleMembers} /> */}
      {/* # 구조: 손님 영역(검색창 + 목록 + 등록 폼)을 부른다. */}
      {/* #       "initialMembers={sampleMembers}"는 "initialMembers라는 이름으로 준비한 재료 상자를 건넨다"는 뜻이다. */}
      {/* #       (Props 전달. 이름 initialMembers는 STEP 02의 MemberWorkspaceProps와 정확히 같아야 한다.) */}
      {/* # 목적: 2강에서는 MemberList를 직접 불렀지만, 이제는 검색·입력 기능이 있는 MemberWorkspace가 대신 받는다. */}
      {/* # 예상결과: 샘플 회원 3명, 검색창, 초기화 버튼, 이름·이메일·나이 폼, 현재 입력값 미리보기가 나타난다. */}
      <MemberWorkspace initialMembers={sampleMembers} />
    </main>
  );
}