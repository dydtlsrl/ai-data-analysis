// ============================================================
// lib/members-api.ts
// ------------------------------------------------------------
// [목적]  백엔드(FastAPI)에 "회원 목록 주세요" 전화를 거는 담당 직원
// [구조]  getMembers() 함수 1개 (화면은 이 함수만 부르면 된다)
// [예상결과] 성공 → Member[] 배열 반환 / 실패 → Error를 던진다
// ============================================================

// # Member 타입(주문서)을 가져온다 → 응답이 이 모양인지 검사할 때 쓴다
import type { Member } from "../types/member";

// # 요청 경로를 상수로 둔다
// # 우리 백엔드는 "/members/" (끝 슬래시 포함). 슬래시가 없으면 307 이동이 일어난다
const MEMBERS_PATH = "/members/";

// # [함수] isMember: 값 하나가 Member 모양인지 검사하는 검수 담당
// #   입력: 정체를 모르는 값(unknown)
// #   처리: 객체인지 확인 → member_id/age는 숫자, name/email은 문자열인지 확인
// #   출력: 맞으면 true, 아니면 false
function isMember(value: unknown): value is Member {
  // # 객체가 아니거나 null이면 바로 탈락
  if (typeof value !== "object" || value === null) {
    return false;
  }

  // # 속성을 읽기 위해 "이름→값" 모양의 객체로 본다
  const item = value as Record<string, unknown>;

  // # 4개 속성의 타입이 모두 맞아야 통과
  return (
    typeof item.member_id === "number" &&
    typeof item.name === "string" &&
    typeof item.email === "string" &&
    typeof item.age === "number"
  );
}

// # [함수] getMembers: 회원 목록을 백엔드에서 가져온다 (비동기)
// #   입력: signal(선택) → "그만 기다려" 신호. 화면이 사라질 때 요청을 취소하는 데 쓴다
// #   처리: 주소 읽기 → fetch(GET) → 상태 확인 → JSON 변환 → 모양 검사
// #   출력: Promise<Member[]>  (async 함수는 항상 Promise를 돌려준다)
export async function getMembers(signal?: AbortSignal): Promise<Member[]> {
  // # 1) 수첩(.env.local)에서 백엔드 주소를 읽는다
  const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  // # 2) 주소가 비어 있으면 어디로 전화할지 모르므로 즉시 오류
  if (!baseUrl) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL이 설정되지 않았습니다.");
  }

  // # 3) 전화 걸기: 주소 끝의 "/"를 정리하고 경로를 붙여 GET 요청
  // #    cache: "no-store" → 저장된 옛 답 말고 항상 새로 받는다
  // #    signal → 취소 신호 연결
  const response = await fetch(
    `${baseUrl.replace(/\/$/, "")}${MEMBERS_PATH}`,
    { cache: "no-store", signal },
  );

  // # 4) 응답이 200번대가 아니면(404, 500 등) 오류로 처리
  if (!response.ok) {
    throw new Error(`회원 조회 실패: HTTP ${response.status}`);
  }

  // # 5) 응답 본문(JSON 글자)을 자바스크립트 값으로 변환
  const data: unknown = await response.json();

  // # 6) 배열이고, 모든 항목이 Member 모양인지 검사
  if (!Array.isArray(data) || !data.every(isMember)) {
    throw new Error("API 응답이 예상한 Member[] 형식이 아닙니다.");
  }

  // # 7) 통과! 회원 배열을 화면에 넘긴다
  return data;
}