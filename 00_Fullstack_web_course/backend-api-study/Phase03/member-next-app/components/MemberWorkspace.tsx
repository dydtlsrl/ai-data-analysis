"use client";

// ============================================================
// components/MemberWorkspace.tsx  (4강 버전)
// ------------------------------------------------------------
// [목적]  FastAPI에서 회원 목록을 받아 검색·표시하고, 등록 폼은 미리보기만 한다
// [구조]  상태 → 조회 함수 → 자동 조회(useEffect) → 검색 필터 → 화면
// [예상결과] 처음 열면 "불러오는 중" → 회원 목록 표시
//           백엔드가 꺼져 있으면 "조회 오류" 문구 + 다시 조회 버튼
// ============================================================

// # useCallback: 함수를 기억해 두는 도구 / useEffect: 화면이 뜬 뒤 실행할 일 / useState: 칠판
import { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";
// # 전화 담당 직원, 점원(목록), 주문서(타입)를 가져온다
import { getMembers } from "../lib/members-api";
import type { Member } from "../types/member";
import MemberList from "./MemberList";

// # [컴포넌트] MemberWorkspace: 이제 props 없이 스스로 데이터를 가져온다
export default function MemberWorkspace() {
  // ---------- 칠판(State) ----------
  // # 서버에서 받은 회원 목록 (처음엔 빈 배열)
  const [members, setMembers] = useState<Member[]>([]);
  // # 기다리는 중인가? (처음 열자마자 조회하니 true로 시작)
  const [loading, setLoading] = useState(true);
  // # 실패 메시지 (빈 문자열이면 오류 없음)
  const [error, setError] = useState("");
  // # "다시 조회" 버튼을 누를 때마다 1씩 커지는 숫자 → useEffect를 다시 실행시키는 신호
  const [reloadKey, setReloadKey] = useState(0);

  // # 검색어와 등록 폼 입력값 (3강과 동일)
  const [search, setSearch] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");

  // ---------- 조회 함수 ----------
  // # [함수] loadMembers: 회원을 조회하고 칠판(State)을 갱신한다
  // #   입력: signal(취소 신호)
  // #   처리: 로딩 켜기 → 조회 → 성공이면 members 저장 / 실패면 error 저장 → 로딩 끄기
  // #   useCallback: 렌더링마다 새 함수가 만들어지지 않도록 하나를 기억해 둔다 ([] = 바뀔 일 없음)
  const loadMembers = useCallback(async (signal: AbortSignal) => {
    setLoading(true); // # 기다리는 중 표시 ON
    setError(""); // # 이전 오류 지우기

    try {
      const data = await getMembers(signal); // # 전화 담당에게 주문
      if (signal.aborted) return; // # 이미 취소된 요청이면 결과 버림
      setMembers(data); // # 성공: 칠판에 회원 저장
    } catch (caught) {
      if (signal.aborted) return; // # 취소로 생긴 오류는 무시
      // # Error 객체면 그 메시지, 아니면 기본 문구
      setError(caught instanceof Error ? caught.message : "알 수 없는 조회 오류");
    } finally {
      // # 성공이든 실패든 마지막엔 로딩 OFF (취소된 요청은 건드리지 않음)
      if (!signal.aborted) setLoading(false);
    }
  }, []);

  // ---------- 자동 조회 ----------
  // # [useEffect] 화면이 뜬 직후, 그리고 reloadKey가 바뀔 때마다 실행
  // #   AbortController: 취소 버튼을 만든다
  // #   return () => abort(): 화면이 사라지거나 다시 실행되기 직전에 이전 요청 취소 (정리 함수)
  useEffect(() => {
    const controller = new AbortController();
    void loadMembers(controller.signal); // # void: 결과를 기다리지 않고 실행만 한다
    return () => controller.abort();
  }, [loadMembers, reloadKey]);

  // ---------- 검색 필터 ----------
  // # 검색어 앞뒤 공백 제거. toLowerCase는 쓰지 않는다 (3강 STEP 06에서 정한 방식 유지)
  const keyword = search.trim();
  // # 이름 또는 이메일에 검색어가 들어 있는 회원만 남긴다 (이제 members 기준)
  const filteredMembers = members.filter(
    (member) => member.name.includes(keyword) || member.email.includes(keyword),
  );

  // ---------- 등록 폼 미리보기 (3강과 동일, API 호출 없음) ----------
  // # 나이가 비어 있지 않고, 정수이고, 0~150 사이면 유효
  const ageNumber = Number(age);
  const validAge =
    age.trim() !== "" && Number.isInteger(ageNumber) && ageNumber >= 0 && ageNumber <= 150;

  // # [함수] handlePreview: 제출 시 새로고침을 막고, 입력값이 유효하면 미리보기를 보여준다
  function handlePreview(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); // # 폼의 기본 동작(페이지 새로고침) 막기
  }

  // ---------- 화면 ----------
  return (
    <section>
      {/* # 검색 영역: 입력창 + 초기화 + 다시 조회 */}
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
        {/* # reloadKey를 1 올리면 useEffect가 다시 실행되어 재조회. 조회 중엔 비활성화 */}
        <button
          type="button"
          onClick={() => setReloadKey((value) => value + 1)}
          disabled={loading}
        >
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

      {/* # 등록 폼 미리보기 (3강 그대로) */}
      <form onSubmit={handlePreview}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="이름" />
        <input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="이메일" />
        <input value={age} onChange={(e) => setAge(e.target.value)} placeholder="나이" />
        <button type="submit">미리보기</button>
      </form>

      {/* # 입력값이 모두 있고 나이가 유효할 때만 미리보기 카드 표시 */}
      {name && email && validAge && (
        <p>
          미리보기: {name} / {email} / {ageNumber}세
        </p>
      )}
    </section>
  );
}