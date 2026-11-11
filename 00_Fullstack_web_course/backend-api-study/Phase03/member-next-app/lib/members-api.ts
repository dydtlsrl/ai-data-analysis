// ============================================================
// lib/members-api.ts  (5강 버전)
// ------------------------------------------------------------
// [목적]  백엔드(FastAPI)에 회원 조회·등록·수정·삭제 전화를 거는 담당 직원
// [구조]  경로 2개 + 보조 함수 3개 + API 함수 4개
// [예상결과] 성공 → 결과 반환 / 실패 → "HTTP 상태코드"가 담긴 Error를 던진다
// ============================================================

// # Member 타입(주문서)을 가져온다
import type { Member } from "../types/member";

// # 요청 경로 2종류 (백엔드 라우터를 확인한 결과)
// #   컬렉션(목록·등록): "/members/"      → 끝 슬래시 있음
// #   항목(수정·삭제):   "/members/{id}"  → 끝 슬래시 없음
// #   이 모양이 아니면 307 이동이나 404가 난다
const MEMBERS_COLLECTION_PATH = "/members/";
const MEMBERS_ITEM_PATH = "/members";

// # 등록·수정 때 서버에 보내는 주문서 모양: Member에서 member_id만 뺀 것
// #   member_id는 서버가 정하므로 보내지 않는다
export type MemberPayload = Pick<Member, "name" | "email" | "age">;

// # [함수] apiUrl: 수첩(.env.local)의 주소 + 경로를 합쳐 완성된 주소를 만든다
// #   입력: path (예: "/members/")
// #   처리: 주소가 없으면 오류 / 주소 끝의 "/"를 정리하고 경로를 붙인다
// #   출력: "http://127.0.0.1:8001/members/" 같은 문자열
function apiUrl(path: string): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;

  // # 수첩이 비어 있으면 어디로 전화할지 모르므로 즉시 오류
  if (!base) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL이 설정되지 않았습니다.");
  }

  return base.replace(/\/$/, "") + path;
}

// # [함수] isMember: 값 하나가 Member 모양인지 검사하는 검수 담당
// #   입력: 정체를 모르는 값(unknown)
// #   처리: 객체인지 확인 → member_id/age는 숫자, name/email은 문자열인지 확인
// #   출력: 맞으면 true, 아니면 false
function isMember(value: unknown): value is Member {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const item = value as Record<string, unknown>;

  return (
    typeof item.member_id === "number" &&
    typeof item.name === "string" &&
    typeof item.email === "string" &&
    typeof item.age === "number"
  );
}

// # [함수] requireOk: 응답이 성공(200번대)인지 확인하는 보조 담당
// #   처리: 실패(404, 409, 422, 500 등)면 상태코드를 담아 오류를 던진다
// #   본문(JSON)은 읽지 않는다 → 204처럼 본문이 없는 성공도 안전하다
function requireOk(response: Response): void {
  if (!response.ok) {
    throw new Error(`회원 API 요청 실패: HTTP ${response.status}`);
  }
}

// # [함수] getMembers: 회원 목록 조회 (GET /members/)  ← 4강과 동일
// #   입력: signal(선택) → 화면이 사라질 때 요청을 취소하는 신호
// #   출력: Promise<Member[]>
export async function getMembers(signal?: AbortSignal): Promise<Member[]> {
  // # cache: "no-store" → 저장된 옛 답 말고 항상 새로 받는다
  const response = await fetch(apiUrl(MEMBERS_COLLECTION_PATH), {
    cache: "no-store",
    signal,
  });

  if (!response.ok) {
    throw new Error(`회원 조회 실패: HTTP ${response.status}`);
  }

  // # 응답 본문(JSON 글자)을 자바스크립트 값으로 변환
  const data: unknown = await response.json();

  // # 배열이고 모든 항목이 Member 모양인지 검사
  if (!Array.isArray(data) || !data.every(isMember)) {
    throw new Error("API 응답이 예상한 Member[] 형식이 아닙니다.");
  }

  return data;
}

// # [함수] createMember: 회원 등록 (POST /members/)  → 성공 201
// #   입력: body = { name, email, age }
// #   처리: JSON 글자로 바꿔 전송 → 성공 확인 (응답 본문은 쓰지 않는다)
// #   출력: Promise<void> (돌려줄 값 없음. 최신 목록은 화면이 GET으로 다시 받는다)
export async function createMember(body: MemberPayload): Promise<void> {
  const response = await fetch(apiUrl(MEMBERS_COLLECTION_PATH), {
    method: "POST", // # 새로 만들어 달라는 방식
    headers: { "Content-Type": "application/json" }, // # "본문은 JSON입니다"라고 알림
    body: JSON.stringify(body), // # 자바스크립트 객체 → JSON 글자
  });

  requireOk(response);
}

// # [함수] updateMember: 회원 수정 (PUT /members/{id})  → 성공 200
// #   입력: memberId(고칠 회원 번호), body = { name, email, age } 전체
// #   처리: PUT은 "전체 교체"라서 3개 필드를 모두 보낸다
// #   출력: Promise<void>
export async function updateMember(
  memberId: number,
  body: MemberPayload,
): Promise<void> {
  const response = await fetch(
    apiUrl(`${MEMBERS_ITEM_PATH}/${memberId}`), // # 예: /members/7
    {
      method: "PUT", // # 전체 교체 방식 (백엔드는 PATCH도 지원하지만 PUT 사용)
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    },
  );

  requireOk(response);
}

// # [함수] deleteMember: 회원 삭제 (DELETE /members/{id})  → 성공 204
// #   입력: memberId(지울 회원 번호)
// #   처리: 204는 본문이 없으므로 response.json()을 부르지 않는다
// #   출력: Promise<void>
export async function deleteMember(memberId: number): Promise<void> {
  const response = await fetch(
    apiUrl(`${MEMBERS_ITEM_PATH}/${memberId}`), // # 예: /members/7
    { method: "DELETE" },
  );

  requireOk(response);
}