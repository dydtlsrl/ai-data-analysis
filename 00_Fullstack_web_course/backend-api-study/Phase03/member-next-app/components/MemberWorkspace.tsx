"use client";

// ============================================================
// components/MemberWorkspace.tsx  (5강 버전)
// ------------------------------------------------------------
// [목적]  회원 조회·검색 + 등록·수정·삭제(CRUD)를 한 화면에서 처리하는 주인
// [구조]  상태 → 자동 조회(useEffect) → 재조회 → 검색 필터 → 폼 검증
//         → 수정 시작 → 등록/수정 제출 → 삭제 → 화면
// [예상결과] 등록/수정/삭제가 성공하면 GET으로 목록을 다시 받아 화면과 DB가 같아진다
//           실패하면 빨간 오류 문구가 나오고 입력값은 유지된다
// ============================================================

import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import MemberList from "./MemberList";
// # 전화 담당 직원 4명 (조회·등록·수정·삭제)
import {
  createMember,
  deleteMember,
  getMembers,
  updateMember,
} from "../lib/members-api";
import type { Member } from "../types/member";

export default function MemberWorkspace() {
  // ---------- 칠판(State) ----------
  // # 서버에서 받은 회원 목록
  const [members, setMembers] = useState<Member[]>([]);
  // # 목록을 불러오는 중인가? / 목록 조회 오류 메시지 / 재조회 신호 숫자
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  // # 검색어
  const [search, setSearch] = useState("");

  // # 폼 입력값 (등록과 수정이 같은 폼을 쓴다)
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [age, setAge] = useState("");

  // # 수정 중인 회원 번호 (null이면 "새로 등록하는 중")
  const [editingId, setEditingId] = useState<number | null>(null);
  // # 등록·수정·삭제 요청을 처리하는 중인가? (true면 버튼 잠금, 중복 클릭 방지)
  const [busy, setBusy] = useState(false);
  // # 등록·수정·삭제 실패 메시지 / 성공 안내 문구
  const [actionError, setActionError] = useState("");
  const [notice, setNotice] = useState("");

  // ---------- 자동 조회 (4강 방식 그대로) ----------
  // # 화면이 뜬 직후, 그리고 reloadKey가 바뀔 때마다 목록을 조회한다
  // # setState는 결과가 돌아온 뒤의 콜백(then/catch/finally) 안에서만 부른다 → eslint 규칙 준수
  useEffect(() => {
    const controller = new AbortController(); // # 취소 버튼

    getMembers(controller.signal)
      .then((data) => {
        if (controller.signal.aborted) return; // # 취소된 요청이면 결과 버림
        setMembers(data);
      })
      .catch((caught: unknown) => {
        if (controller.signal.aborted) return;
        setLoadError(caught instanceof Error ? caught.message : "알 수 없는 조회 오류");
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });

    return () => controller.abort(); // # 정리 함수: 이전 요청 취소
  }, [reloadKey]);

  // ---------- 다시 조회 (버튼 클릭 핸들러) ----------
  // # 로딩 켜기·오류 지우기는 여기서 한다 (effect 안에서 하면 eslint가 막는다)
  function handleReload() {
    setLoading(true);
    setLoadError("");
    setReloadKey((value) => value + 1);
  }

  // ---------- 검색 필터 (3강 방식 유지: toLowerCase 없음) ----------
  const keyword = search.trim();
  const filteredMembers = members.filter(
    (member) => member.name.includes(keyword) || member.email.includes(keyword),
  );

  // ---------- 폼 검증 ----------
  // # 나이: 비어 있지 않고, 정수이고, 0~150
  const ageNumber = Number(age);
  const validAge =
    age.trim() !== "" && Number.isInteger(ageNumber) && ageNumber >= 0 && ageNumber <= 150;
  // # 이름·이메일이 비어 있지 않고 나이가 유효해야 제출 가능
  const validForm = name.trim() !== "" && email.trim() !== "" && validAge;

  // # [함수] clearForm: 폼을 비우고 "등록 모드"로 되돌린다
  function clearForm() {
    setEditingId(null);
    setName("");
    setEmail("");
    setAge("");
  }

  // # [함수] startEdit: 카드의 수정 버튼이 눌렸을 때, 그 회원 값을 폼에 채우고 "수정 모드"로 바꾼다
  function startEdit(member: Member) {
    setEditingId(member.member_id);
    setName(member.name);
    setEmail(member.email);
    setAge(String(member.age)); // # 입력창은 문자열이므로 숫자를 문자열로 바꾼다
    setActionError("");
    setNotice("");
  }

  // # [함수] handleSubmit: 폼 제출 → 등록(POST) 또는 수정(PUT) → 성공하면 GET으로 재조회
  // #   editingId가 null이면 등록, 숫자면 수정
  // #   changed: "서버 변경은 성공했는가?" 표시. 재조회만 실패한 경우를 구별하려고 쓴다
  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault(); // # 페이지 새로고침 막기
    if (!validForm || busy || loading) return; // # 잘못된 입력·처리 중이면 아무것도 안 함

    setBusy(true);
    setActionError("");
    setNotice("");
    let changed = false;
    const action = editingId === null ? "등록" : "수정";

    try {
      const payload = { name: name.trim(), email: email.trim(), age: ageNumber };

      if (editingId === null) {
        await createMember(payload); // # POST
      } else {
        await updateMember(editingId, payload); // # PUT
      }
      changed = true; // # 여기까지 오면 서버 변경은 성공

      const latest = await getMembers(); // # GET 재조회: 서버의 최신 목록
      setMembers(latest);
      clearForm();
      setNotice(`회원 ${action} 후 목록을 다시 조회했습니다.`);
    } catch (error) {
      const detail = error instanceof Error ? error.message : "알 수 없는 오류";
      setActionError(
        changed
          ? `서버 변경 요청은 성공했으나 목록 재조회에 실패했습니다: ${detail}`
          : `회원 ${action} 요청 실패: ${detail}`,
      );
    } finally {
      setBusy(false); // # 성공이든 실패든 버튼 잠금 해제
    }
  }

  // # [함수] handleDelete: 카드의 삭제 버튼 → 확인 창 → 삭제(DELETE) → 성공하면 GET으로 재조회
  async function handleDelete(member: Member) {
    if (busy || loading) return;

    // # 실수 방지: 확인 창에서 취소하면 DELETE 요청을 보내지 않는다
    if (!window.confirm(`${member.name} 회원(ID ${member.member_id})을 삭제할까요?`)) {
      return;
    }

    setBusy(true);
    setActionError("");
    setNotice("");
    let changed = false;

    try {
      await deleteMember(member.member_id); // # DELETE (성공 204, 본문 없음)
      changed = true;

      const latest = await getMembers(); // # GET 재조회
      setMembers(latest);
      // # 지금 수정 중이던 회원을 지웠다면 폼도 비운다
      if (editingId === member.member_id) clearForm();
      setNotice("회원 삭제 후 목록을 다시 조회했습니다.");
    } catch (error) {
      const detail = error instanceof Error ? error.message : "알 수 없는 오류";
      setActionError(
        changed
          ? `서버 삭제 요청은 성공했으나 목록 재조회에 실패했습니다: ${detail}`
          : `회원 삭제 요청 실패: ${detail}`,
      );
    } finally {
      setBusy(false);
    }
  }

  // ---------- 화면 ----------
  return (
    <div>
      {/* # 검색 영역: 입력창 + 검색 초기화 + 다시 조회 */}
      <section style={{ marginTop: 28 }}>
        <label htmlFor="member-search">회원 검색 (이름 또는 이메일)</label>
        <div>
          <input
            id="member-search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="예: kim"
            style={{ padding: 10, marginRight: 8 }}
          />
          <button type="button" onClick={() => setSearch("")}>
            검색 초기화
          </button>{" "}
          {/* # 조회 중이거나 처리 중이면 비활성화 */}
          <button type="button" disabled={loading || busy} onClick={handleReload}>
            다시 조회
          </button>
        </div>
      </section>

      {/* # 3분기: 로딩 중 → 조회 오류 → 목록 (목록에는 수정·삭제 알림 통로를 이어 준다) */}
      {loading ? (
        <p role="status">회원 목록을 불러오는 중입니다...</p>
      ) : loadError ? (
        <p role="alert" style={{ color: "#b91c1c" }}>
          목록 조회 오류: {loadError}
        </p>
      ) : (
        <MemberList
          members={filteredMembers}
          onEdit={startEdit}
          onDelete={(member) => {
            void handleDelete(member); // # void: 결과를 기다리지 않고 실행만 한다
          }}
          busy={busy}
        />
      )}

      {/* # 등록/수정 폼: editingId에 따라 제목과 버튼 글자가 바뀐다 */}
      <section
        style={{
          marginTop: 36,
          padding: 20,
          border: "1px solid #cbd5e1",
          borderRadius: 12,
        }}
      >
        <h2>{editingId === null ? "회원 등록" : `회원 수정 (ID ${editingId})`}</h2>
        <p>실제 서버에 저장됩니다. 반드시 테스트 회원만 사용하세요.</p>

        <form
          onSubmit={(event) => {
            void handleSubmit(event);
          }}
        >
          <label htmlFor="member-name">이름</label>
          <input
            id="member-name"
            value={name}
            onChange={(event) => setName(event.target.value)}
            required
            style={{ display: "block", padding: 10, marginBottom: 14 }}
          />

          <label htmlFor="member-email">이메일</label>
          <input
            id="member-email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
            style={{ display: "block", padding: 10, marginBottom: 14 }}
          />

          <label htmlFor="member-age">나이</label>
          <input
            id="member-age"
            type="number"
            min={0}
            max={150}
            value={age}
            onChange={(event) => setAge(event.target.value)}
            required
            style={{ display: "block", padding: 10, marginBottom: 14 }}
          />

          {/* # 입력이 유효하지 않거나 처리 중이면 제출 버튼 비활성화 */}
          <button type="submit" disabled={!validForm || busy || loading}>
            {busy ? "처리 중..." : editingId === null ? "회원 등록" : "회원 수정 저장"}
          </button>{" "}
          <button type="button" disabled={busy} onClick={clearForm}>
            입력 초기화 / 수정 취소
          </button>
        </form>

        {/* # 성공 안내(초록) / 실패 오류(빨강) */}
        {notice && (
          <p role="status" style={{ color: "#166534" }}>
            {notice}
          </p>
        )}
        {actionError && (
          <p role="alert" style={{ color: "#b91c1c" }}>
            {actionError}
          </p>
        )}
      </section>
    </div>
  );
}