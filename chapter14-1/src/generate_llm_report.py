import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from ollama import Client


BASE_DIR = Path(__file__).resolve().parents[1]
REPORTS_DIR = BASE_DIR / "reports"
SUMMARY_PATH = REPORTS_DIR / "analysis_summary.csv"
OUTPUT_PATH = REPORTS_DIR / "llm_summary.md"

load_dotenv(BASE_DIR / ".env")


def load_summary() -> list[dict]:
    """Python에서 검증한 분석 요약 CSV를 LLM 입력 형태로 변환합니다."""
    if not SUMMARY_PATH.exists():
        raise FileNotFoundError(f"분석 요약 파일이 없습니다: {SUMMARY_PATH}")

    summary = pd.read_csv(SUMMARY_PATH)
    required_columns = {"source", "period", "item", "metric", "value"}
    missing_columns = required_columns - set(summary.columns)
    if missing_columns:
        raise RuntimeError(
            f"분석 요약 파일에 필요한 열이 없습니다: {sorted(missing_columns)}"
        )
    if summary.empty:
        raise RuntimeError("분석 요약 파일이 비어 있습니다.")

    # pandas의 NaN을 JSON에서 안전하게 표현할 수 있는 None으로 바꿉니다.
    clean_summary = summary.astype(object).where(pd.notna(summary), None)
    return clean_summary.to_dict(orient="records")


def build_prompt(summary: list[dict]) -> str:
    """검증된 숫자를 바꾸지 못하도록 역할과 작성 규칙을 명확히 지정합니다."""
    naver_rows = [row for row in summary if row["metric"] == "search_interest_ratio"]
    stay_rows = [row for row in summary if row["metric"] == "stay_intensity"]
    consumption_rows = [
        row for row in summary if row["metric"] == "consumption_intensity"
    ]

    naver_facts = "\n".join(
        (
            f"- {row['item']}: 최신 상대지수 {float(row['value']):.2f}, "
            f"전월 대비 {float(row['change_from_previous']):+.2f} 지수 포인트"
        )
        for row in naver_rows
    )
    stay_facts = "\n".join(
        f"{index}. {row['item']}: {float(row['value']):.2f}"
        for index, row in enumerate(stay_rows, start=1)
    )
    consumption_facts = "\n".join(
        f"{index}. {row['item']}: {float(row['value']):.2f}"
        for index, row in enumerate(consumption_rows, start=1)
    )

    stay_names = [str(row["item"]) for row in stay_rows]
    consumption_names = [str(row["item"]) for row in consumption_rows]
    common_names = [name for name in stay_names if name in set(consumption_names)]
    stay_only_names = [name for name in stay_names if name not in set(consumption_names)]
    consumption_only_names = [
        name for name in consumption_names if name not in set(stay_names)
    ]

    naver_period = str(naver_rows[0]["period"])
    tourism_period = str(stay_rows[0]["period"])

    return f"""
당신은 데이터 분석 보고서를 작성하는 보조자입니다.
아래 문장은 Python으로 계산하고 반올림까지 마친 확정 사실입니다.
숫자를 다시 계산하지 말고 표시된 값을 그대로 복사하세요.

<확정_사실>
[NAVER 검색 관심도]
- 기준일: {naver_period}
{naver_facts}

[관광 체류 강도 상위 10개 지역]
- 기준월: {tourism_period}
{stay_facts}

[관광 소비 강도 상위 10개 지역]
- 기준월: {tourism_period}
{consumption_facts}

[두 상위 10개 목록의 확정 비교]
- 공통 지역 {len(common_names)}개: {', '.join(common_names)}
- 체류 강도 상위 10개에만 있는 지역: {', '.join(stay_only_names)}
- 소비 강도 상위 10개에만 있는 지역: {', '.join(consumption_only_names)}
</확정_사실>

다음 구조의 한국어 Markdown 보고서를 작성하세요.

# 관광 트렌드 분석 보고서
## 1. 분석 기준
## 2. 검색 관심도 주요 변화
## 3. 관광 체류 강도 주요 지역
## 4. 관광 소비 강도 주요 지역
## 5. 관찰 가능한 패턴
## 6. 데이터의 한계
## 7. 추가로 확인할 사항

작성 규칙:
- 확정 사실에 표시된 숫자만 정확히 복사해서 사용하세요.
- 검색 관심도 ratio는 실제 검색 건수가 아닌 상대지수라고 명시하세요.
- 검색 관심도를 비율, 퍼센트, 검색량이라고 부르지 말고 반드시 상대지수라고 표현하세요.
- 전월 대비 값은 퍼센트가 아니라 두 상대지수의 차이인 '지수 포인트'입니다.
- 예를 들어 -1.66 지수 포인트를 -16.6%나 -1.66%로 쓰면 안 됩니다.
- 검색 관심도와 관광 지표 사이의 인과관계를 단정하지 마세요.
- 관광 지표의 기준월을 명확히 적으세요.
- 확인되지 않은 지역, 수치, 사건을 만들어내지 마세요.
- 체류 강도와 소비 강도는 각각 상위 10개 지역을 빠짐없이 순서대로 적으세요.
- 서울 전체 25개 자치구가 수집되었으며 위에는 상위 10개만 요약되어 있습니다.
- 따라서 지역 데이터가 누락되었다고 표현하지 마세요.
- 입력에 없는 지리적 특성(중심부, 외곽, 상권 등)을 추측하지 마세요.
- 관찰 가능한 패턴은 위의 '두 상위 10개 목록의 확정 비교'만 그대로 설명하세요.
- 목록 포함 여부를 이중 부정으로 표현하지 마세요.
- 핵심 수치를 포함하되 초보자도 이해하기 쉬운 문장으로 작성하세요.
- 모델의 생각 과정이나 내부 추론은 출력하지 말고 완성된 보고서만 출력하세요.
""".strip()


def call_ollama(prompt: str) -> str:
    """내 PC에서 실행 중인 Ollama 모델에 보고서 작성을 요청합니다."""
    provider = os.getenv("LLM_PROVIDER", "").strip().lower()
    model = os.getenv("LLM_MODEL", "").strip()
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434").strip()

    if provider != "ollama":
        raise RuntimeError("LLM_PROVIDER를 ollama로 설정하세요.")
    if not model:
        raise RuntimeError("LLM_MODEL이 설정되지 않았습니다.")

    client = Client(host=host, timeout=300.0)
    response = client.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "당신은 제공된 데이터만 근거로 보고서를 작성합니다. "
                    "숫자를 변경하거나 사실을 추측하지 않습니다."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        stream=False,
        think=True,
        keep_alive="10m",
        options={"temperature": 0.2},
    )

    text = response.message.content.strip()
    if not text:
        raise RuntimeError("Ollama가 빈 응답을 반환했습니다.")
    return text


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    summary = load_summary()
    prompt = build_prompt(summary)
    report = call_ollama(prompt)

    OUTPUT_PATH.write_text(report + "\n", encoding="utf-8")

    print("[PASS] Local LLM Report")
    print("model:", os.getenv("LLM_MODEL"))
    print("input rows:", len(summary))
    print("saved:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
