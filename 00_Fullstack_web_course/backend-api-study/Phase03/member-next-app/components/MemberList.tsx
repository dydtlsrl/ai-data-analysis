// ============================================================
// components/MemberList.tsx  (5강 버전)
// ------------------------------------------------------------
// [목적]  회원 카드들을 목록으로 보여 주고, 카드의 수정·삭제 알림을 위로 전달한다
// [구조]  Props 타입 → 컴포넌트(제목 + 비었을 때 문구 / 카드 줄 세우기)
// [예상결과] 회원 N명 → 카드 N장 (각 카드에 수정/삭제 버튼)
//           회원 0명 → "등록된 회원이 없습니다."
// ============================================================

// # Member 타입(주문서)과 카드(붕어빵 틀)를 가져온다
import type { Member } from "../types/member";
import MemberCard from "./MemberCard";

// # [타입] MemberListProps: 이 점원이 받는 재료(Props)의 약속
// #   members  : 보여 줄 회원 배열
// #   onEdit   : 카드의 수정 버튼 알림을 위로 전달할 함수
// #   onDelete : 카드의 삭제 버튼 알림을 위로 전달할 함수
// #   busy     : 서버와 통신 중이면 true (카드의 버튼 잠금용)
type MemberListProps = {
  members: Member[];
  onEdit: (member: Member) => void;
  onDelete: (member: Member) => void;
  busy: boolean;
};

// # [컴포넌트] MemberList: 회원 배열을 카드 목록으로 바꿔 그린다
export default function MemberList({
  members,
  onEdit,
  onDelete,
  busy,
}: MemberListProps) {
  return (
    <section aria-labelledby="member-list-title" style={{ marginTop: 32 }}>
      {/* # 제목: 현재 보이는 회원 수를 함께 표시 */}
      <h2 id="member-list-title" style={{ color: "#0f172a" }}>
        회원 목록 ({members.length}명)
      </h2>

      {/* # 삼항 연산자: 회원이 0명이면 안내 문구, 있으면 카드 목록 */}
      {members.length === 0 ? (
        <p style={{ color: "#64748b" }}>등록된 회원이 없습니다.</p>
      ) : (
        <ul style={{ display: "grid", gap: 12, padding: 0 }}>
          {/* # map: 회원 1명 → 카드 1장. key는 React가 카드를 구별하는 이름표(member_id) */}
          {members.map((member) => (
            <MemberCard
              key={member.member_id}
              member={member}
              onEdit={onEdit} // # 카드의 수정 알림을 그대로 위로 전달
              onDelete={onDelete} // # 카드의 삭제 알림을 그대로 위로 전달
              busy={busy} // # 처리 중 상태를 카드에 내려 준다
            />
          ))}
        </ul>
      )}
    </section>
  );
}