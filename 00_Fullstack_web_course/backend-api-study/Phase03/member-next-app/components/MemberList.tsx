// ==================================================================
// # 파일: components/MemberList.tsx
// # 역할: 회원 "여러 명"을 받아서 MemberCard를 한 명당 하나씩 찍어내는 점원
// # 흐름: 부모가 members(재료 목록)를 건네줌 → 하나씩 꺼냄 → 틀(MemberCard)에 넣음 → 카드 여러 장
// ==================================================================

// # [명령어] import type { Member } from "../types/member";
// # 목적: 주문서 양식(Member)을 가져온다. 이 파일에서는 "Member가 여러 개 모인 목록"을 다룬다.
import type { Member } from "../types/member";

// # [명령어] import MemberCard from "./MemberCard";
// # 구조: "./"는 같은 폴더(components)를 뜻한다. 중괄호 { } 가 없는 import는 그 파일이 대표로 내보낸(export default) 것을 가져온다.
// # 목적: STEP 03에서 만든 붕어빵 틀을 이 파일에서 쓰려고 가져온다.
// # 예상결과: 아래에서 <MemberCard ... /> 를 태그처럼 쓸 수 있다.
import MemberCard from "./MemberCard";

// # [명령어] type MemberListProps = { members: Member[]; };
// # 구조: 부모가 건네줄 택배 상자(Props)의 설명서다.
// #       "Member[]"에서 [ ]는 "Member가 여러 개 담긴 목록(배열)"이라는 뜻이다.
// #       (Member = 한 명, Member[] = 여러 명)
// # 예상결과: 화면에는 보이지 않는다. 설명서일 뿐이다.
type MemberListProps = {
  members: Member[];
};

// # [명령어] export default function MemberList({ members }: MemberListProps) { ... }
// # 구조: 받은 택배 상자(Props)를 열어 members(회원 목록)만 꺼내 쓴다.
// # 목적: 이 점원이 회원 목록을 받아 카드를 여러 장 만든다.
export default function MemberList({ members }: MemberListProps) {
  return (
    // # [태그] <section aria-labelledby="member-list-title" style={{ marginTop: 32 }}>
    // # 구조: <section>은 주제별로 묶는 구역 상자다. marginTop 32는 위쪽 간격이다.
    // #       aria-labelledby는 화면 읽기 프로그램(시각장애인용)에게 "이 구역의 제목은 id가 member-list-title인 곳"이라고 알려주는 이름표다.
    // # 예상결과: 보이는 모양에는 영향이 없다. 위쪽에 간격만 생긴다.
    <section aria-labelledby="member-list-title" style={{ marginTop: 32 }}>
      {/* # [태그] <h2 id="member-list-title"> : 구역의 제목 */}
      {/* # 구조: {members.length}는 "목록에 몇 명이 들어 있는지" 숫자를 센 값이다. */}
      {/* #       id는 위 section의 이름표(aria-labelledby)와 짝을 이룬다. */}
      {/* # 예상결과: 3명이 들어오면 "회원 목록 (3명)", 0명이면 "회원 목록 (0명)" */}
      <h2 id="member-list-title" style={{ fontSize: 24, color: "#0f172a" }}>
        회원 목록 ({members.length}명)
      </h2>

      {/* # [문법] 조건 ? A : B  (삼항 연산자) */}
      {/* # 구조: "조건이 참이면 A를, 거짓이면 B를 보여줘라"는 뜻이다. */}
      {/* #       members.length === 0 은 "목록이 0명인가?"라는 질문이다. (=== 는 '같은가?') */}
      {/* # 목적: 회원이 없을 때 빈 화면 대신 안내문을 보여주려고 한다. */}
      {/* # 예상결과: 0명이면 안내문 한 줄, 1명 이상이면 카드 목록이 나온다. */}
      {members.length === 0 ? (
        // # [A: 0명일 때] 안내문 한 줄만 보여준다.
        <p style={{ color: "#64748b" }}>등록된 회원이 없습니다.</p>
      ) : (
        // # [B: 1명 이상일 때] 카드들을 담을 목록 상자(<ul>)를 만든다.
        // # 구조: display "grid"는 칸 배치 방식이고, gap 12는 카드 사이 12px 간격이다.
        // #       padding 0은 <ul>의 기본 왼쪽 들여쓰기를 없앤다.
        // # 예상결과: 카드가 세로로 쭉 쌓이고, 카드 사이에 간격이 생긴다.
        <ul style={{ display: "grid", gap: 12, padding: 0 }}>
          {/* # [메서드] members.map((member) => ( ... )) */}
          {/* # 구조: members 목록에서 회원을 한 명씩 꺼내 member라 부르고, */}
          {/* #       그때마다 괄호 안의 결과물(MemberCard)을 만들어 모은다. */}
          {/* # 목적: 회원 수가 늘어나도 코드를 고치지 않고 카드가 자동으로 늘어난다. */}
          {/* # 예상결과: Kim → Lee → Park 순서로 MemberCard 3개가 만들어진다. */}
          {members.map((member) => (
            // # [속성] key={member.member_id}
            // # 구조: 반복해서 만든 카드마다 서로 다른 이름표를 붙인다. 회원 번호는 겹치지 않아 이름표로 알맞다.
            // # 목적: React가 "어떤 카드가 바뀌었는지" 구분하게 한다.
            // # 예상결과: 화면에는 안 보인다. 번호가 겹치면 콘솔에 key 경고가 뜬다.
            // # [속성] member={member}
            // # 구조: "member라는 이름으로, 지금 꺼낸 회원(member)을 틀에 건네준다"는 뜻이다. (Props 전달)
            // # 예상결과: MemberCard가 그 회원의 이름, 이메일, 나이, ID로 카드를 만든다.
            <MemberCard key={member.member_id} member={member} />
          ))}
        </ul>
      )}
    </section>
  );
}