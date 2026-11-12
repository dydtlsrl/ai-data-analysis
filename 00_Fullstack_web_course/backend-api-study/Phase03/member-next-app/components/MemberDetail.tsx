"use client";

// ============================================================
// components/MemberDetail.tsx  (6강: 새 파일)
// ------------------------------------------------------------
// [목적]  주소의 회원 번호로 FastAPI에서 회원 1명을 조회해 보여 준다
// [구조]  주소에서 번호 읽기 → 번호 검증 → 조회(useEffect) → 화면(번호오류/로딩/오류/성공)
// [예상결과] /members/2  → 2번 회원 정보 표시
//           /members/abc → "올바른 회원 ID" 안내 (서버 요청 없음)
//           /members/4   → 없는 회원이면 "조회 오류: HTTP 404"
// ============================================================

import { useEffect, useState } from "react";
import Link from "next/link";
// # useParams: 주소의 [memberId] 자리에 들어온 값을 읽는 도구
import { useParams } from "next/navigation";
import { getMember } from "../lib/members-api";
import type { Member } from "../types/member";

// # [타입] DetailResult: 조회 결과 + "어느 회원 번호의 결과인지" 이름표(id)
// #   이름표가 있어야 주소가 바뀌었을 때 이전 회원 결과를 새 주소에 잘못 보여 주지 않는다
type DetailResult = {
  id: number;
  member: Member | null;
  error: string;
};

export default function MemberDetail() {
  // ---------- 주소에서 번호 읽기 ----------
  // # 주소가 /members/2 이면 memberIdText는 "2" (항상 글자로 온다)
  const params = useParams<{ memberId: string }>();
  const memberIdText = params.memberId;
  const memberId = Number(memberIdText);

  // # 번호 검증: 숫자만(0~9)으로 이루어졌고, 안전한 정수이고, 1 이상일 때만 유효
  // # "abc", "-1", "1.5", "0" 은 서버에 보내지 않고 막는다
  const validId =
    /^\d+$/.test(memberIdText) && Number.isSafeInteger(memberId) && memberId > 0;

  // ---------- 칠판(State) ----------
  // # 마지막 조회 결과 (처음엔 null)
  const [result, setResult] = useState<DetailResult | null>(null);

  // ---------- 자동 조회 ----------
  // # 화면이 뜬 직후, 그리고 회원 번호가 바뀔 때마다 실행
  // # setState는 결과가 돌아온 뒤 콜백(then/catch) 안에서만 부른다 → eslint 규칙 준수
  // # 정리 함수(return): 번호가 바뀌거나 화면이 사라질 때 이전 요청 취소
  useEffect(() => {
    if (!validId) return; // # 잘못된 번호면 서버에 요청하지 않는다

    const controller = new AbortController();

    getMember(memberId, controller.signal)
      .then((member) => {
        if (controller.signal.aborted) return; // # 취소된 요청이면 결과 버림
        setResult({ id: memberId, member, error: "" });
      })
      .catch((caught: unknown) => {
        if (controller.signal.aborted) return;
        setResult({
          id: memberId,
          member: null,
          error: caught instanceof Error ? caught.message : "회원 상세 조회 오류",
        });
      });

    return () => controller.abort();
  }, [memberId, validId]);

  // ---------- 파생 값 (State로 따로 저장하지 않는다) ----------
  // # 이름표가 지금 번호와 같은 결과만 "현재 결과"로 인정한다
  const current = result !== null && result.id === memberId ? result : null;
  // # 번호는 맞는데 현재 결과가 아직 없으면 기다리는 중
  const loading = validId && current === null;

  // ---------- 화면 ----------
  return (
    <section>
      <h1>회원 상세</h1>
      <p>
        <Link href="/members">← 회원 목록으로 돌아가기</Link>
      </p>

      {/* # 4분기: 번호 오류 → 로딩 → 조회 오류 → 성공 */}
      {!validId ? (
        <p role="alert">올바른 회원 ID를 입력해 주세요.</p>
      ) : loading ? (
        <p role="status">회원 정보를 불러오는 중입니다...</p>
      ) : current?.error ? (
        <p role="alert" style={{ color: "#b91c1c" }}>
          조회 오류: {current.error}
        </p>
      ) : current?.member ? (
        <div
          style={{
            backgroundColor: "#fff",
            border: "1px solid #cbd5e1",
            borderRadius: 12,
            padding: 24,
          }}
        >
          <p style={{ color: "#64748b" }}>회원 ID: {current.member.member_id}</p>
          <h2 style={{ color: "#0f172a" }}>{current.member.name}</h2>
          <p style={{ color: "#334155" }}>이메일: {current.member.email}</p>
          <p style={{ color: "#334155" }}>나이: {current.member.age}세</p>
        </div>
      ) : (
        <p role="alert">회원 정보를 찾을 수 없습니다.</p>
      )}
    </section>
  );
}