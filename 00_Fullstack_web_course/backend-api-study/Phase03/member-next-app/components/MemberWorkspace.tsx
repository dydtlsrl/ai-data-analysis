// ==================================================================
// # 파일: components/MemberWorkspace.tsx
// # 역할: 손님이 만지는 영역(검색창 + 등록 연습 폼)을 담당하는 부품
// # 핵심 구조: 칠판(State)에 값을 적어 둔다 → 손님이 입력하면(Event) 칠판을 고친다
// #            → 칠판이 바뀌면 화면이 자동으로 다시 그려진다
// ==================================================================

// # [명령어] "use client";
// # 구조: 파일 맨 위에 적는 표시. "이 파일은 손님이 직접 만지는 영역(브라우저)에서 동작한다"는 뜻이다.
// # 목적: useState와 onChange 같은 "입력·클릭 처리"는 이 표시가 있어야 쓸 수 있다.
// # 예상결과: 이 줄이 없으면 useState를 쓰는 순간 Next.js가 오류를 낸다.
"use client";

// # [명령어] import { useState } from "react";
// # 구조: React가 제공하는 도구 중 useState(칠판 만드는 도구)만 꺼내 온다.
// #       { } 중괄호는 "여러 개 중에 이름을 지정해서 꺼내 온다"는 표시다.
// # 목적: 검색어, 이름, 이메일, 나이를 기억할 칠판을 만들려고 가져온다.
import { useState } from "react";

// # [명령어] import type { FormEvent } from "react";
// # 구조: "폼에서 일어난 사건(제출)의 모양"이라는 약속(type)만 가져온다.
// # 목적: 아래 handlePreview 함수가 받는 event의 자료형을 정확히 적어 두려고 쓴다.
import type { FormEvent } from "react";

// # [명령어] import MemberList from "./MemberList";
// # 목적: 2강에서 만든 점원(MemberList)을 가져온다. 이 파일은 점원에게 걸러진 목록을 건네줄 것이다.
import MemberList from "./MemberList";

// # [명령어] import type { Member } from "../types/member";
// # 목적: 주문서 양식(Member)을 가져온다. 회원 목록의 자료형을 정확히 적기 위해 쓴다.
import type { Member } from "../types/member";

// # [명령어] type MemberWorkspaceProps = { initialMembers: Member[]; };
// # 구조: 부모(page.tsx)가 건네줄 택배 상자(Props)의 설명서다.
// #       "initialMembers: Member[]"는 "처음 보여줄 회원 여러 명이 initialMembers라는 이름으로 온다"는 뜻이다.
// # 예상결과: 화면에는 안 보인다. 설명서일 뿐이다.
type MemberWorkspaceProps = {
  initialMembers: Member[];
};

// # [명령어] export default function MemberWorkspace({ initialMembers }: MemberWorkspaceProps) { ... }
// # 구조: 받은 택배 상자(Props)를 열어 initialMembers(처음 회원 목록)만 꺼내 쓴다. (2강과 같은 방식)
export default function MemberWorkspace({
  initialMembers,
}: MemberWorkspaceProps) {
  // ==================================================================
  // # [칠판 만들기] 기억해야 할 값 4개를 칠판(State)에 적어 둔다
  // ==================================================================

  // # [명령어] const [search, setSearch] = useState("");
  // # 구조: useState("")는 "칠판을 만들고 처음엔 빈 글자(\"\")를 적어 두라"는 뜻이다.
  // #       결과로 2개를 돌려준다 → [지금 칠판에 적힌 값, 칠판을 고치는 지우개+펜].
  // #       그래서 const [search, setSearch] 는 "값은 search, 고치는 도구는 setSearch"라고 이름을 붙인 것이다.
  // # 목적: 검색창에 손님이 친 글자를 기억해 둔다.
  // # 예상결과: 처음에는 search가 빈 글자라서 목록이 전부 보인다.
  // # 주의: search = "kim" 처럼 직접 바꾸면 안 된다. 반드시 setSearch("kim")으로 고쳐야 화면이 다시 그려진다.
  const [search, setSearch] = useState("");

  // # 이름, 이메일, 나이도 같은 방식이다. 처음엔 모두 빈 글자다.
  // # (나이도 처음엔 "" 글자로 둔다. 입력칸에서 나오는 값은 항상 글자이기 때문이다.)
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");

  // ==================================================================
  // # [검색 계산] 칠판의 검색어에 맞는 회원만 걸러낸다
  // ==================================================================

  // # [명령어] const filteredMembers = initialMembers.filter((member) => { ... });
  // # 구조: "목록.filter(...)"는 목록에서 한 명씩 꺼내 조건에 맞는 사람만 남겨 새 목록을 만든다.
  // #       (member) => { ... } 는 "꺼낸 회원을 member라 부르고 아래 조건을 검사하라"는 화살표 함수다.
  // #       조건이 참(true)이면 남기고, 거짓(false)이면 뺀다.
  // # 목적: 검색어에 따라 보여줄 회원 목록을 만든다. (원본 initialMembers는 그대로 둔다)
  // # 예상결과: search가 "kim"이면 Kim 1명만 남은 새 목록이 만들어진다.
  const filteredMembers = initialMembers.filter((member) => {
    // # [명령어] const keyword = search.trim().toLowerCase();
    // # 구조: search(검색어)에서 .trim()으로 앞뒤 공백을 지우고, .toLowerCase()로 전부 소문자로 바꾼다.
    // # 목적: " KIM " 이라고 쳐도 "kim"으로 맞춰서, 대소문자와 공백에 상관없이 찾게 한다.
    // # 예상결과: "  LEE " → "lee"
    const keyword = search.trim().toLowerCase();

    // # [명령어] return ( 이름에_포함 || 이메일에_포함 );
    // # 구조: member.name.toLowerCase()로 이름을 소문자로 바꾼 뒤 .includes(keyword)로
    // #       "keyword가 들어 있는가?"를 묻는다. 이메일도 같은 방식이다.
    // #       || 는 "또는"이다. 이름에 있거나 이메일에 있으면 참이다.
    // # 목적: 이름이든 이메일이든 한쪽에만 맞아도 검색 결과에 남긴다.
    // # 예상결과: "kim" → Kim 남음 / "example.com" → 전원 남음 / 빈 글자("") → 전원 남음
    // #           (빈 글자는 모든 글자에 "들어 있다"고 판단하기 때문에 전원이 보인다)
    return (
      member.name.toLowerCase().includes(keyword) ||
      member.email.toLowerCase().includes(keyword)
    );
  });

  // ==================================================================
  // # [입력 검사] 나이 칸에 올바른 값이 들어왔는지 확인한다
  // ==================================================================

  // # [명령어] const ageNumber = Number(age);
  // # 구조: Number(...)는 글자를 숫자로 바꾼다. "25" → 25, "abc" → NaN(숫자 아님)
  // # 목적: 나이는 글자로 저장되어 있으니, 범위를 검사하려면 숫자로 바꿔야 한다.
  const ageNumber = Number(age);

  // # [명령어] const validAge = 조건1 && 조건2 && 조건3 && 조건4;
  // # 구조: && 는 "그리고"다. 네 조건이 모두 참이어야 validAge가 true가 된다.
  // #       age.trim() !== ""        → 칸이 비어 있지 않은가? (!== 는 "같지 않은가?")
  // #       Number.isInteger(...)    → 소수가 아닌 정수인가?
  // #       ageNumber >= 0           → 0 이상인가?
  // #       ageNumber <= 150         → 150 이하인가?
  // # 목적: 이상한 나이(빈칸, 소수, 음수, 200)를 걸러내 버튼 활성화와 미리보기에 사용한다.
  // # 예상결과: "25" → true / "" → false / "-3" → false / "200" → false
  const validAge =
    age.trim() !== "" &&
    Number.isInteger(ageNumber) &&
    ageNumber >= 0 &&
    ageNumber <= 150;

  // ==================================================================
  // # [제출 처리] 폼의 "입력값 확인" 버튼을 눌렀을 때 실행되는 함수
  // ==================================================================

  // # [명령어] function handlePreview(event: FormEvent<HTMLFormElement>) { ... }
  // # 구조: handlePreview라는 이름의 함수. 괄호 안 event는 "방금 일어난 제출 사건"이고,
  // #       ": FormEvent<HTMLFormElement>"는 그 사건의 모양을 적어 둔 약속이다.
  // # 목적: 폼 제출 때의 동작을 우리가 직접 정한다.
  function handlePreview(event: FormEvent<HTMLFormElement>) {
    // # [명령어] event.preventDefault();
    // # 구조: "브라우저의 기본 동작을 막아라"는 명령이다. 폼 제출의 기본 동작은 "페이지 새로고침"이다.
    // # 목적: 새로고침되면 칠판(State)에 적어 둔 값이 전부 사라지기 때문에 막는다.
    // # 예상결과: 버튼을 눌러도 화면이 깜빡이지 않고 그대로 유지된다.
    event.preventDefault();

    // # [명령어] if (조건) { return; }
    // # 구조: "이름이 비었거나, 이메일이 비었거나, 나이가 올바르지 않으면 여기서 함수를 끝내라"
    // #       !값 은 "아니라면"이다. !name.trim() = 이름이 비어 있으면.
    // # 목적: 올바르지 않은 입력으로 아래 단계로 넘어가지 않게 막는다.
    if (!name.trim() || !email.trim() || !validAge) {
      return;
    }

    // # [주석] 3강: API 요청/DB 저장은 하지 않습니다.
    // # 이 함수는 여기서 아무 일도 하지 않고 끝난다. 실제 저장은 5강에서 이 자리에 추가한다.
  }

  // ==================================================================
  // # [화면 그리기]
  // ==================================================================
  return (
    // # [태그] <div> : 전체를 감싸는 빈 상자
    <div>
      {/* # ============ 1) 검색 영역 ============ */}
      {/* # [태그] <section style={{ marginTop: 28 }}> : 검색창 구역. 위쪽에 간격 28px */}
      <section style={{ marginTop: 28 }}>
        {/* # [태그] <label htmlFor="member-search"> : 입력칸에 붙이는 이름표 글자 */}
        {/* # 구조: htmlFor는 "id가 member-search인 입력칸의 이름표"라는 연결이다. */}
        {/* # 목적: 이름표 글자를 클릭해도 입력칸에 커서가 가고, 화면 읽기 프로그램도 알아본다. */}
        {/* # 예상결과: "회원 검색 (이름 또는 이메일)" 글자가 입력칸 위에 보인다. */}
        <label htmlFor="member-search" style={{ display: "block", marginBottom: 8 }}>
          회원 검색 (이름 또는 이메일)
        </label>

        {/* # [태그] <input id="member-search" value={search} onChange={...} /> : 검색 입력칸 */}
        {/* # 구조: value={search}    → 입력칸에 보이는 글자는 칠판(search)에 적힌 값이다. */}
        {/* #       onChange={(event) => setSearch(event.target.value)} */}
        {/* #         → 글자가 바뀔 때마다 실행된다. event.target.value는 "입력칸에 지금 적힌 글자"다. */}
        {/* #           그 글자로 칠판(search)을 고친다. */}
        {/* #       placeholder → 비어 있을 때 흐리게 보이는 안내 글자 */}
        {/* # 목적: "칠판 = 입력칸"이 항상 똑같도록 이어 놓는다. (이걸 Controlled Form이라 부른다) */}
        {/* # 예상결과: k, i, m을 치는 순간마다 search가 "k", "ki", "kim"으로 바뀌고 목록이 즉시 줄어든다. */}
        <input
          id="member-search"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="예: kim"
          style={{ width: "min(100%, 360px)", padding: 10, border: "1px solid #94a3b8", borderRadius: 8 }}
        />

        {/* # [태그] <button type="button" onClick={() => setSearch("")}> : 초기화 버튼 */}
        {/* # 구조: type="button" → 폼 제출 버튼이 아닌 그냥 버튼이라는 표시 */}
        {/* #       onClick={() => setSearch("")} → 클릭하면 칠판(search)을 빈 글자로 되돌린다. */}
        {/* # 예상결과: 클릭하면 입력칸이 비워지고 회원 3명이 다시 보인다. */}
        <button
          type="button"
          onClick={() => setSearch("")}
          style={{ marginLeft: 8, padding: "10px 14px", cursor: "pointer" }}
        >
          초기화
        </button>
      </section>

      {/* # ============ 2) 회원 목록 ============ */}
      {/* # [핵심] <MemberList members={filteredMembers} /> */}
      {/* # 구조: 2강에서 만든 점원을 부른다. 이번에는 전체 회원이 아니라 "걸러진 회원 목록"을 건넨다. */}
      {/* # 목적: MemberList 코드는 한 줄도 안 고쳤는데, 건네는 재료만 바뀌어서 화면이 달라진다. (Props의 힘) */}
      {/* # 예상결과: "kim" → "회원 목록 (1명)" / 없는 이름 → "회원 목록 (0명)"과 안내문 */}
      <MemberList members={filteredMembers} />

      {/* # ============ 3) 등록 연습 폼 ============ */}
      {/* # [태그] <section style={{ ... }}> : 테두리 있는 폼 구역 */}
      <section
        style={{
          marginTop: 36,
          padding: 20,
          border: "1px solid #cbd5e1",
          borderRadius: 12,
        }}
      >
        <h2 style={{ marginTop: 0 }}>회원 등록 연습 (미리보기)</h2>

        <p style={{ color: "#64748b" }}>
          아직 저장 기능이 없습니다. 입력값만 확인합니다.
        </p>

        {/* # [태그] <form onSubmit={handlePreview}> : 입력칸들을 묶는 폼 */}
        {/* # 구조: onSubmit={handlePreview} → 제출될 때 위에서 만든 handlePreview 함수를 실행한다. */}
        {/* #       제출 = 제출 버튼 클릭 또는 입력칸에서 Enter */}
        {/* # 예상결과: 제출하면 새로고침 없이 그대로 유지된다. (preventDefault 덕분) */}
        <form onSubmit={handlePreview}>
          {/* # [이름 입력칸] 검색창과 같은 원리: value는 칠판(name), onChange는 칠판 고치기(setName) */}
          {/* # required → 비어 있으면 브라우저가 제출을 막고 "입력하세요" 안내를 보여준다. */}
          <label htmlFor="member-name">이름</label>
          <input
            id="member-name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Hong"
            required
            style={{ display: "block", padding: 10, margin: "6px 0 16px", width: "min(100%, 360px)" }}
          />

          {/* # [이메일 입력칸] type="email" → 브라우저가 이메일 모양(@ 포함)인지 확인해 준다. */}
          <label htmlFor="member-email">이메일</label>
          <input
            id="member-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="hong@example.com"
            required
            style={{ display: "block", padding: 10, margin: "6px 0 16px", width: "min(100%, 360px)" }}
          />

          {/* # [나이 입력칸] type="number" → 숫자만 입력. min/max는 브라우저가 알려주는 범위(0~150) */}
          {/* # 주의: 숫자칸이어도 event.target.value는 항상 "글자"로 나온다. 그래서 위에서 Number()로 바꿨다. */}
          <label htmlFor="member-age">나이</label>
          <input
            id="member-age"
            type="number"
            min={0}
            max={150}
            value={age}
            onChange={(event) => setAge(event.target.value)}
            placeholder="25"
            required
            style={{ display: "block", padding: 10, margin: "6px 0 16px", width: "min(100%, 360px)" }}
          />

          {/* # [태그] <button type="submit" disabled={...}> : 입력값 확인 버튼 */}
          {/* # 구조: type="submit" → 이 버튼을 누르면 폼이 제출된다. */}
          {/* #       disabled={조건} → 조건이 참이면 버튼이 눌리지 않게 회색으로 막는다. */}
          {/* #       !name.trim() || !email.trim() || !validAge → 이름 없음 또는 이메일 없음 또는 나이 오류 */}
          {/* # 예상결과: 세 칸이 모두 올바르게 채워지는 순간 버튼이 활성화된다. */}
          {/* # 참고: 눌러도 눈에 보이는 변화는 없다. (미리보기는 입력하는 즉시 이미 바뀌어 있다) */}
          <button
            type="submit"
            disabled={!name.trim() || !email.trim() || !validAge}
            style={{ padding: "10px 14px" }}
          >
            입력값 확인
          </button>
        </form>

        {/* # [태그] <p role="status"> : 현재 입력값을 보여주는 미리보기 */}
        {/* # 구조: role="status"는 화면 읽기 프로그램에게 "이 글이 바뀌면 알려 줘"라는 표시 */}
        {/* #       {name.trim() || "(이름 없음)"} → 이름이 있으면 이름, 비어 있으면 "(이름 없음)" */}
        {/* #         (|| 는 "앞이 비었으면 뒤를 써라"로도 쓰인다) */}
        {/* #       {validAge ? ageNumber + "세" : "(나이 ...)"} → 올바른 나이면 "25세", 아니면 안내 글자 */}
        {/* #       {" "} → 줄바꿈 때문에 사라지는 띄어쓰기를 일부러 한 칸 넣는 표시 */}
        {/* # 예상결과: Hong을 치면 즉시 "Hong / (이메일 없음) / (나이 미입력 또는 범위 오류)"로 바뀐다. */}
        <p role="status" style={{ marginTop: 20 }}>
          <strong>현재 입력값:</strong>{" "}
          {name.trim() || "(이름 없음)"} /{" "}
          {email.trim() || "(이메일 없음)"} /{" "}
          {validAge ? ageNumber + "세" : "(나이 미입력 또는 범위 오류)"}
        </p>

        <p style={{ color: "#b45309", fontWeight: 600 }}>
          학습용 미리보기이며 저장되지 않습니다.
        </p>
      </section>
    </div>
  );
}