// ============================================================
// components/MemberCard.tsx  (6강 버전)
// ------------------------------------------------------------
// [목적]  회원 1명을 카드로 보여 주고, 상세 이동 링크와 수정·삭제 "의사"를 제공한다
// [구조]  Props 타입 → 컴포넌트(정보 + 상세 보기 링크 + 버튼 2개)
// [예상결과] 카드에 "상세 보기 / 수정 / 삭제"가 보이고, 상세 보기를 누르면 /members/ID 로 이동한다
// ============================================================

// # Link: 새로고침 없이 Next.js 방식으로 페이지를 이동시키는 링크
import Link from "next/link";
import type { Member } from "../types/member";

// # [타입] MemberCardProps: 5강과 동일 (Props는 늘리지 않는다)
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
      {/* # 이름 / 이메일 / 나이·ID 표시 */}
      <h3 style={{ margin: "0 0 8px", color: "#0f172a" }}>{member.name}</h3>
      <p style={{ color: "#334155" }}>{member.email}</p>
      <p style={{ color: "#64748b" }}>
        나이 {member.age}세 · ID {member.member_id}
      </p>

      {/* # 상세 보기: 주소가 "/members/회원번호"로 바뀐다 (예: /members/2) */}
      <Link href={`/members/${member.member_id}`}>상세 보기</Link>{" "}

      {/* # 수정 버튼: 눌리면 onEdit(이 회원)을 호출해 위로 알린다. busy면 비활성화 */}
      <button type="button" disabled={busy} onClick={() => onEdit(member)}>
        수정
      </button>{" "}

      {/* # 삭제 버튼: 눌리면 onDelete(이 회원)을 호출해 위로 알린다 */}
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