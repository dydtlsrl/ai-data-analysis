import re
from datetime import date
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"
LLM_REPORT_PATH = REPORTS_DIR / "llm_summary.md"
NAVER_CHART_PATH = REPORTS_DIR / "naver_trend.png"
TOURISM_CHART_PATH = REPORTS_DIR / "tourism_consumption_top10.png"

TODAY = date.today().isoformat()
PDF_PATH = REPORTS_DIR / f"tourism_trend_report_{TODAY}.pdf"

FONT_PATH = Path(r"C:\Windows\Fonts\malgun.ttf")
BOLD_FONT_PATH = Path(r"C:\Windows\Fonts\malgunbd.ttf")

PAGE_WIDTH, PAGE_HEIGHT = A4
CONTENT_WIDTH = PAGE_WIDTH - 36 * mm

NAVY = colors.HexColor("#16324F")
BLUE = colors.HexColor("#2F6690")
LIGHT_BLUE = colors.HexColor("#EAF2F8")
GRAY = colors.HexColor("#5B6573")
LIGHT_GRAY = colors.HexColor("#D9E1E8")


def register_fonts() -> None:
    """Windows의 맑은 고딕을 PDF에 포함해 한글 깨짐을 방지합니다."""
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"맑은 고딕 글꼴을 찾을 수 없습니다: {FONT_PATH}")
    if not BOLD_FONT_PATH.exists():
        raise FileNotFoundError(f"맑은 고딕 굵은 글꼴을 찾을 수 없습니다: {BOLD_FONT_PATH}")

    pdfmetrics.registerFont(TTFont("MalgunGothic", str(FONT_PATH)))
    pdfmetrics.registerFont(TTFont("MalgunGothicBold", str(BOLD_FONT_PATH)))


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "KoreanTitle",
            parent=base["Title"],
            fontName="MalgunGothicBold",
            fontSize=24,
            leading=32,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=10 * mm,
        ),
        "subtitle": ParagraphStyle(
            "KoreanSubtitle",
            parent=base["Normal"],
            fontName="MalgunGothic",
            fontSize=10,
            leading=16,
            textColor=GRAY,
            alignment=TA_CENTER,
        ),
        "heading1": ParagraphStyle(
            "KoreanHeading1",
            parent=base["Heading1"],
            fontName="MalgunGothicBold",
            fontSize=16,
            leading=23,
            textColor=NAVY,
            spaceBefore=8 * mm,
            spaceAfter=4 * mm,
            keepWithNext=True,
        ),
        "heading2": ParagraphStyle(
            "KoreanHeading2",
            parent=base["Heading2"],
            fontName="MalgunGothicBold",
            fontSize=13,
            leading=20,
            textColor=BLUE,
            spaceBefore=6 * mm,
            spaceAfter=3 * mm,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "KoreanBody",
            parent=base["BodyText"],
            fontName="MalgunGothic",
            fontSize=9.5,
            leading=16,
            textColor=colors.HexColor("#202832"),
            alignment=TA_LEFT,
            spaceAfter=2.2 * mm,
            wordWrap="CJK",
        ),
        "bullet": ParagraphStyle(
            "KoreanBullet",
            parent=base["BodyText"],
            fontName="MalgunGothic",
            fontSize=9.5,
            leading=16,
            textColor=colors.HexColor("#202832"),
            leftIndent=5 * mm,
            firstLineIndent=-4 * mm,
            spaceAfter=1.5 * mm,
            wordWrap="CJK",
        ),
        "caption": ParagraphStyle(
            "KoreanCaption",
            parent=base["Normal"],
            fontName="MalgunGothic",
            fontSize=8.5,
            leading=13,
            textColor=GRAY,
            alignment=TA_CENTER,
            spaceBefore=2 * mm,
            spaceAfter=5 * mm,
        ),
        "callout": ParagraphStyle(
            "KoreanCallout",
            parent=base["BodyText"],
            fontName="MalgunGothic",
            fontSize=9,
            leading=15,
            textColor=NAVY,
            backColor=LIGHT_BLUE,
            borderColor=LIGHT_GRAY,
            borderWidth=0.6,
            borderPadding=8,
            spaceBefore=4 * mm,
            spaceAfter=5 * mm,
            wordWrap="CJK",
        ),
    }


def inline_markdown(text: str) -> str:
    """보고서에 사용된 간단한 Markdown 굵은 글씨를 ReportLab 형식으로 바꿉니다."""
    safe = escape(text.strip())
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", safe)


def markdown_to_flowables(markdown: str, styles: dict[str, ParagraphStyle]) -> list:
    """LLM Markdown의 제목, 본문, 목록을 PDF 문단으로 변환합니다."""
    flowables = []

    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            flowables.append(Spacer(1, 1.5 * mm))
            continue

        # 문서 제목은 표지에서 이미 출력하므로 중복하지 않습니다.
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            flowables.append(Paragraph(inline_markdown(line[3:]), styles["heading2"]))
        elif line.startswith("- "):
            flowables.append(
                Paragraph("- " + inline_markdown(line[2:]), styles["bullet"])
            )
        elif re.match(r"^\d+\.\s", line):
            flowables.append(Paragraph(inline_markdown(line), styles["bullet"]))
        else:
            flowables.append(Paragraph(inline_markdown(line), styles["body"]))

    return flowables


def scaled_image(path: Path, max_width: float, max_height: float) -> Image:
    """원본 비율을 유지하면서 PDF 페이지 안에 맞게 이미지를 축소합니다."""
    image = Image(str(path))
    scale = min(max_width / image.imageWidth, max_height / image.imageHeight)
    image.drawWidth = image.imageWidth * scale
    image.drawHeight = image.imageHeight * scale
    image.hAlign = "CENTER"
    return image


def draw_page_frame(canvas, document) -> None:
    """모든 페이지에 상단선, 문서명, 페이지 번호를 표시합니다."""
    canvas.saveState()
    canvas.setStrokeColor(LIGHT_GRAY)
    canvas.setLineWidth(0.6)
    canvas.line(18 * mm, PAGE_HEIGHT - 14 * mm, PAGE_WIDTH - 18 * mm, PAGE_HEIGHT - 14 * mm)

    canvas.setFont("MalgunGothic", 7.5)
    canvas.setFillColor(GRAY)
    canvas.drawString(18 * mm, 10 * mm, "관광 트렌드 자동 분석 보고서")
    canvas.drawRightString(
        PAGE_WIDTH - 18 * mm,
        10 * mm,
        f"{canvas.getPageNumber()} page",
    )
    canvas.restoreState()


def validate_inputs() -> str:
    required_files = [LLM_REPORT_PATH, NAVER_CHART_PATH, TOURISM_CHART_PATH]
    missing_files = [str(path) for path in required_files if not path.exists()]
    if missing_files:
        raise FileNotFoundError("필요한 보고서 파일이 없습니다: " + ", ".join(missing_files))

    markdown = LLM_REPORT_PATH.read_text(encoding="utf-8").strip()
    if not markdown:
        raise RuntimeError("LLM 보고서가 비어 있습니다.")
    return markdown


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    register_fonts()
    styles = build_styles()
    markdown = validate_inputs()

    document = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title="관광 트렌드 자동 분석 보고서",
        author="AI Data Analysis",
        subject="NAVER 검색 관심도와 서울 관광 지표 분석",
    )

    story = [
        Spacer(1, 20 * mm),
        Paragraph("관광 트렌드 자동 분석 보고서", styles["title"]),
        Paragraph(
            "NAVER 검색 관심도와 서울 지역 관광 체류·소비 강도 분석",
            styles["subtitle"],
        ),
        Spacer(1, 8 * mm),
        HRFlowable(width="70%", thickness=1.2, color=BLUE, hAlign="CENTER"),
        Spacer(1, 8 * mm),
        Paragraph(f"보고서 생성일: {TODAY}", styles["subtitle"]),
        Spacer(1, 14 * mm),
        Paragraph(
            "본 보고서는 Python이 계산·검증한 결과를 로컬 LLM이 문장으로 정리한 자료입니다. "
            "검색 관심도는 실제 검색 건수가 아닌 상대지수이며, 검색과 관광 지표의 관계를 "
            "인과관계로 해석하지 않습니다.",
            styles["callout"],
        ),
        PageBreak(),
    ]

    story.extend(markdown_to_flowables(markdown, styles))

    story.extend(
        [
            PageBreak(),
            Paragraph("시각화 1. NAVER 검색 관심도 추이", styles["heading1"]),
            scaled_image(NAVER_CHART_PATH, CONTENT_WIDTH, 155 * mm),
            Paragraph(
                "조회 기간 내 키워드별 상대 검색 관심도 변화를 나타냅니다. "
                "값은 실제 검색 건수가 아니라 조회 조건 안에서의 상대지수입니다.",
                styles["caption"],
            ),
            PageBreak(),
            Paragraph("시각화 2. 관광 소비 강도 상위 지역", styles["heading1"]),
            scaled_image(TOURISM_CHART_PATH, CONTENT_WIDTH, 155 * mm),
            Paragraph(
                "공공데이터포털 관광 소비 강도 지표를 기준으로 정렬한 상위 10개 서울 자치구입니다.",
                styles["caption"],
            ),
        ]
    )

    document.build(
        story,
        onFirstPage=draw_page_frame,
        onLaterPages=draw_page_frame,
    )

    print("[PASS] PDF Report")
    print("saved:", PDF_PATH)


if __name__ == "__main__":
    main()
