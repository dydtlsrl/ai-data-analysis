// ============================================================
// components/MemberCard.tsx  (5강 버전)
// ------------------------------------------------------------
// [목적]  회원 1명을 카드 1장으로 보여 주고, 수정·삭제 "의사"를 위로 알린다
// [구조]  Props 타입 → 컴포넌트(정보 표시 + 버튼 2개)
// [예상결과] 카드마다 수정/삭제 버튼이 보인다
//           처리 중(busy=true)에는 두 버튼이 눌리지 않는다
// ============================================================

// # Member 타입(주문서)을 가져온다
import type { Member } from "../types/member";

// # [타입] MemberCardProps: 이 카드가 받는 재료(Props)의 약속
// #   member   : 보여 줄 회원 1명
// #   onEdit   : "수정 버튼이 눌렸다"를 알리는 함수 (회원을 함께 넘긴다)
// #   onDelete : "삭제 버튼이 눌렸다"를 알리는 함수 (회원을 함께 넘긴다)
// #   busy     : 서버와 통신 중이면 true → 버튼 잠금
type MemberCardProps = {
  member: Member;
  onEdit: (member: Member) => void;
  onDelete: (member: Member) => void;
  busy: boolean;
};

// # [컴포넌트] MemberCard: Props를 받아 카드 1장을 그린다
export default function MemberCard({
  member,
  onEdit,
  onDelete,
  busy,
}: MemberCardProps) {
  return (
    <li
      style={{
        listStyle: "none",
        padding: 20,
        backgroundColor: "#fff",
        border: "1px solid #cbd5e1",
        borderRadius: 12,
      }}
    >
      {/* # 이름 / 이메일 / 나이·ID 표시 (2강과 동일) */}
      <h3 style={{ margin: "0 0 8px", color: "#0f172a" }}>{member.name}</h3>
      <p style={{ color: "#334155" }}>{member.email}</p>
      <p style={{ color: "#64748b" }}>
        나이 {member.age}세 · ID {member.member_id}
      </p>

      {/* # 수정 버튼: 눌리면 onEdit(이 회원)을 호출해 위로 알린다. busy면 비활성화 */}
      <button type="button" disabled={busy} onClick={() => onEdit(member)}>
        수정
      </button>{" "}

      {/* # 삭제 버튼: 눌리면 onDelete(이 회원)을 호출해 위로 알린다. 글자색을 빨갛게 해 위험을 표시 */}
      <button
        type="button"
        disabled={busy}
        onClick={() => onDelete(member)}
        style={{ color: "#b91c1c" }}
      >
        삭제
      </button>
    </li>
  );
}