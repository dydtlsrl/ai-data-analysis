"use client";

// ============================================================
// components/MemberWorkspace.tsx  (4강 최종 버전 v2)
// ------------------------------------------------------------
// [목적]  FastAPI에서 회원 목록을 받아 검색·표시하고, 등록 폼은 미리보기만 한다
// [구조]  상태 → 자동 조회(useEffect) → 다시 조회 → 검색 필터 → 폼 미리보기 → 화면
// [예상결과] 처음 열면 "불러오는 중" → 회원 목록 표시
//           백엔드가 꺼져 있으면 "조회 오류" 문구 + 다시 조회 버튼으로 복구
// ============================================================

// # useEffect: 화면이 뜬 뒤 실행할 일 / useState: 칠판
import { useEffect, useState } from "react";
import type { FormEvent } from "react";
// # 전화 담당 직원, 주문서(타입), 점원(목록)
import { getMembers } from "../lib/members-api";
import type { Member } from "../types/member";
import MemberList from "./MemberList";

// # [컴포넌트] MemberWorkspace: props 없이 스스로 데이터를 가져온다
export default function MemberWorkspace() {
  // ---------- 칠판(State) ----------
  // # 서버에서 받은 회원 목록 (처음엔 빈 배열)
  const [members, setMembers] = useState<Member[]>([]);
  // # 기다리는 중인가? (열자마자 조회하니 true로 시작)
  const [loading, setLoading] = useState(true);
  // # 실패 메시지 (빈 문자열이면 오류 없음)
  const [error, setError] = useState("");
  // # "다시 조회"를 누를 때마다 1씩 커지는 숫자 → useEffect 재실행 신호
  const [reloadKey, setReloadKey] = useState(0);

  // # 검색어와 등록 폼 입력값
  const [search, setSearch] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");
  // # 미리보기 카드에 보여줄 값 (null이면 아직 미리보기 없음)
  const [previewMember, setPreviewMember] = useState<Omit<Member, "member_id"> | null>(null);

  // ---------- 자동 조회 ----------
  // # [useEffect] 화면이 뜬 직후, 그리고 reloadKey가 바뀔 때마다 실행
  // #   처리: 전화 담당(getMembers)에게 주문 → 결과가 오면(then/catch/finally 콜백) 칠판 갱신
  // #   setState를 "콜백 안"에서만 부르므로 eslint 규칙(effect 안 동기 setState 금지)을 지킨다
  // #   정리 함수(return): 다시 실행되거나 화면이 사라지기 전에 이전 요청을 취소한다
  useEffect(() => {
    const controller = new AbortController(); // # 취소 버튼 만들기

    getMembers(controller.signal)
      .then((data) => {
        if (controller.signal.aborted) return; // # 취소된 요청이면 결과 버림
        setMembers(data); // # 성공: 칠판에 회원 저장
      })
      .catch((caught: unknown) => {
        if (controller.signal.aborted) return; // # 취소로 생긴 오류는 무시
        setError(caught instanceof Error ? caught.message : "알 수 없는 조회 오류");
      })
      .finally(() => {
        // # 성공이든 실패든 마지막엔 로딩 OFF (취소된 요청은 건드리지 않음)
        if (!controller.signal.aborted) setLoading(false);
      });

    return () => controller.abort();
  }, [reloadKey]);

  // ---------- 다시 조회 ----------
  // # [함수] handleReload: 버튼 클릭 시 로딩을 켜고 오류를 지운 뒤 reloadKey를 올린다
  // #   이벤트 핸들러 안의 setState는 규칙 위반이 아니다 (effect 안이 아니므로)
  function handleReload() {
    setLoading(true);
    setError("");
    setReloadKey((value) => value + 1);
  }

  // ---------- 검색 필터 ----------
  // # 검색어 앞뒤 공백 제거 (toLowerCase는 쓰지 않는다: 3강 STEP 06에서 정한 방식 유지)
  const keyword = search.trim();
  // # 이름 또는 이메일에 검색어가 들어 있는 회원만 남긴다
  const filteredMembers = members.filter(
    (member) => member.name.includes(keyword) || member.email.includes(keyword),
  );

  // ---------- 등록 폼 미리보기 (API 호출 없음) ----------
  // # 나이: 비어 있지 않고, 정수이고, 0~150 사이면 유효
  const ageNumber = Number(age);
  const validAge =
    age.trim() !== "" && Number.isInteger(ageNumber) && ageNumber >= 0 && ageNumber <= 150;

  // # [함수] handlePreview: 제출 시 새로고침을 막고, 입력이 유효하면 미리보기를 저장한다
  function handlePreview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); // # 폼 기본 동작(페이지 새로고침) 막기
    // # 이름·이메일이 비었거나 나이가 잘못되면 미리보기를 지우고 종료
    if (!name.trim() || !email.trim() || !validAge) {
      setPreviewMember(null);
      return;
    }
    // # 유효하면 미리보기 값을 칠판에 적는다
    setPreviewMember({ name: name.trim(), email: email.trim(), age: ageNumber });
  }

  // ---------- 화면 ----------
  return (
    <section>
      {/* # 검색 영역: 입력창 + 검색 초기화 + 다시 조회 */}
      <div>
        <input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="이름 또는 이메일 검색"
        />
        {/* # 검색어만 비운다 */}
        <button type="button" onClick={() => setSearch("")}>
          검색 초기화
        </button>
        {/* # 재조회. 조회 중에는 비활성화 */}
        <button type="button" onClick={handleReload} disabled={loading}>
          다시 조회
        </button>
      </div>

      {/* # 3분기: 로딩 중 → 오류 → 목록 */}
      {loading ? (
        <p role="status">회원 목록을 불러오는 중입니다...</p>
      ) : error ? (
        <p role="alert" style={{ color: "crimson" }}>
          조회 오류: {error}
        </p>
      ) : (
        <MemberList members={filteredMembers} />
      )}

      {/* # 등록 폼 (미리보기만, 서버로 보내지 않음) */}
      <form onSubmit={handlePreview}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="이름" />
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="이메일" />
        <input value={age} onChange={(e) => setAge(e.target.value)} placeholder="나이" />
        <button type="submit">미리보기</button>
      </form>

      {/* # 미리보기 값이 있을 때만 표시 */}
      {previewMember && (
        <p>
          미리보기: {previewMember.name} / {previewMember.email} / {previewMember.age}세
        </p>
      )}
    </section>
  );
}