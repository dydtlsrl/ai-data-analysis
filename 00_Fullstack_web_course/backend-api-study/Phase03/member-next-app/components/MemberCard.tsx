// ==================================================================
// # 파일: components/MemberCard.tsx
// # 역할: 회원 "한 명"을 카드 한 장으로 보여주는 붕어빵 틀
// # 흐름: 부모가 member(재료)를 건네줌 → 이 틀에 넣음 → 카드 한 장 완성
// ==================================================================

// # [명령어] import type { Member } from "../types/member";
// # 구조: "import"는 다른 파일에 있는 것을 가져온다는 뜻이다.
// #       { Member }는 가져올 이름, from 뒤는 파일 위치다.
// #       "../"는 한 칸 위 폴더로 올라간다는 뜻이다. (components → member-next-app → types)
// #       "import type"은 값이 아니라 "약속(양식)"만 가져온다는 표시다.
// # 목적: STEP 02에서 만든 주문서 양식(Member)을 이 파일에서도 쓰려고 가져온다.
// # 예상결과: 아래에서 Member를 마음대로 쓸 수 있다. 경로가 틀리면 빨간 줄이 생긴다.
import type { Member } from "../types/member";

// # [명령어] type MemberCardProps = { member: Member; };
// # 구조: 부모가 이 틀에 건네줄 택배 상자(Props)의 설명서다.
// #       "member: Member"는 "상자 안에는 member라는 이름으로 회원 한 명(Member 모양)이 들어 있다"는 뜻이다.
// # 목적: 부모가 회원 한 명이 아니라 엉뚱한 걸 건네면 VS Code가 미리 알려준다.
// # 예상결과: 화면에는 보이지 않는다. (설명서일 뿐)
type MemberCardProps = {
  member: Member;
};

// # [명령어] export default function MemberCard({ member }: MemberCardProps) { ... }
// # 구조: MemberCard라는 이름의 함수(틀)를 만들어 내보낸다.
// #       괄호 안 "{ member }: MemberCardProps"는
// #       "받은 택배 상자(Props)를 열어서 member만 꺼내 쓰겠다. 상자 설명서는 MemberCardProps다"라는 뜻이다.
// # 목적: 부모가 건네준 회원 한 명(member)을 이 틀 안에서 사용한다.
// # 예상결과: 아직은 아무도 이 틀을 부르지 않아서 브라우저 화면은 그대로다. (STEP 05에서 연결한다)
export default function MemberCard({ member }: MemberCardProps) {
  // # [명령어] return ( ... )
  // # 구조: 이 틀로 찍어낸 결과물(화면 설계도)을 돌려준다.
  // # 예상결과: 부모가 이 설계도를 받아 화면에 붙인다.
  return (
    // # [태그] <li style={{ ... }}>
    // # 구조: <li>는 목록(ul) 안의 항목 하나다. 카드 한 장 = 목록의 항목 하나.
    // #       listStyle "none": 항목 앞의 점(•)을 없앤다.
    // #       backgroundColor: 카드 배경색(흰색)
    // #       border: 테두리, borderRadius: 모서리 둥글기, padding: 카드 안쪽 여백
    // # 예상결과: 흰 배경에 얇은 테두리와 둥근 모서리의 카드 모양이 나온다.
    <li
      style={{
        listStyle: "none",
        backgroundColor: "#ffffff",
        border: "1px solid #cbd5e1",
        borderRadius: 12,
        padding: 20,
      }}
    >
      {/* # [태그] <h3> : 소제목 크기의 글자 (카드의 제목 역할) */}
      {/* # 구조: {member.name}은 "중괄호 안의 값을 이 자리에 출력하라"는 뜻이다. */}
      {/*       member는 받은 회원 한 명, .name은 그 회원의 이름 칸이다. */}
      {/* # 예상결과: Kim 재료가 들어오면 "Kim", Lee 재료가 들어오면 "Lee"가 보인다. */}
      <h3 style={{ color: "#0f172a", margin: "0 0 8px" }}>
        {member.name}
      </h3>

      {/* # [태그] <p> : 이메일 한 줄 */}
      {/* # 구조: margin "0 0 8px"은 위 0, 좌우 0, 아래 8px 간격이다. */}
      {/* # 예상결과: 이름 아래에 kim@example.com 같은 이메일이 보인다. */}
      <p style={{ color: "#334155", margin: "0 0 8px" }}>
        {member.email}
      </p>

      {/* # [태그] <p> : 나이와 ID를 한 줄에 */}
      {/* # 구조: "나이 {member.age}세"처럼 글자와 {값}을 섞어 쓸 수 있다. */}
      {/* # 예상결과: "나이 30세 · ID 1" 형태로 보인다. */}
      <p style={{ color: "#64748b", margin: 0 }}>
        나이 {member.age}세 · ID {member.member_id}
      </p>
    </li>
  );
}