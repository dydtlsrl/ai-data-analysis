import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
REPORTS_DIR = BASE_DIR / "reports"

NAVER_PATH = PROCESSED_DIR / "naver_trend.csv"
NAVER_CHART_PATH = REPORTS_DIR / "naver_trend.png"
TOURISM_CHART_PATH = REPORTS_DIR / "tourism_consumption_top10.png"
SUMMARY_PATH = REPORTS_DIR / "analysis_summary.csv"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Windows에서 그래프의 한글이 깨지지 않도록 설정합니다.
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


def find_latest_file(pattern: str) -> Path:
    """data/raw에서 패턴과 일치하는 가장 최근 파일을 찾습니다."""
    files = list(RAW_DIR.glob(pattern))
    if not files:
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {pattern}")
    return max(files, key=lambda path: path.stat().st_mtime)


def load_tourism_items(path: Path) -> pd.DataFrame:
    """공공데이터포털 응답 JSON에서 실제 데이터 목록을 꺼냅니다."""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        header = data["response"]["header"]
        body = data["response"]["body"]
    except (KeyError, TypeError) as exc:
        raise RuntimeError(f"관광 API 응답 구조가 올바르지 않습니다: {path.name}") from exc

    if str(header.get("resultCode")) != "0000":
        raise RuntimeError(
            f"관광 API 오류: {header.get('resultCode')} {header.get('resultMsg')}"
        )

    items = body.get("items", {}).get("item", [])
    if isinstance(items, dict):
        items = [items]
    if not items:
        raise RuntimeError(f"관광 API 결과가 비어 있습니다: {path.name}")

    return pd.DataFrame(items)


# 1. NAVER 검색 관심도 분석
if not NAVER_PATH.exists():
    raise FileNotFoundError(f"NAVER CSV가 없습니다: {NAVER_PATH}")

naver = pd.read_csv(NAVER_PATH)
required_naver_columns = {"period", "keyword", "ratio"}
missing_naver_columns = required_naver_columns - set(naver.columns)
if missing_naver_columns:
    raise RuntimeError(f"NAVER CSV 필드가 부족합니다: {sorted(missing_naver_columns)}")

naver["period"] = pd.to_datetime(naver["period"], errors="coerce")
naver["ratio"] = pd.to_numeric(naver["ratio"], errors="coerce")
if naver[["period", "ratio"]].isna().any().any():
    raise RuntimeError("NAVER CSV에 날짜 또는 숫자로 변환할 수 없는 값이 있습니다.")

naver = naver.sort_values(["keyword", "period"]).copy()
naver["previous_ratio"] = naver.groupby("keyword")["ratio"].shift(1)
naver["change_from_previous"] = naver["ratio"] - naver["previous_ratio"]

latest_naver = (
    naver.groupby("keyword", as_index=False)
    .tail(1)
    .sort_values("ratio", ascending=False)
)

plt.figure(figsize=(10, 6))
for keyword, group in naver.groupby("keyword"):
    group = group.sort_values("period")
    plt.plot(group["period"], group["ratio"], marker="o", label=keyword)

plt.title("NAVER 검색 관심도 추이")
plt.xlabel("기간")
plt.ylabel("상대 관심도")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(NAVER_CHART_PATH, dpi=150)
plt.close()


# 2. 관광 체류·소비 강도 분석
stay_path = find_latest_file("tourism_stay_*.json")
consumption_path = find_latest_file("tourism_consumption_*.json")

stay = load_tourism_items(stay_path)
consumption = load_tourism_items(consumption_path)

required_stay_columns = {
    "baseYm",
    "areaNm",
    "signguNm",
    "tarSjrnDsIxVal",
}
required_consumption_columns = {
    "baseYm",
    "areaNm",
    "signguNm",
    "tarExpDsIxVal",
}

missing_stay_columns = required_stay_columns - set(stay.columns)
missing_consumption_columns = required_consumption_columns - set(consumption.columns)
if missing_stay_columns:
    raise RuntimeError(f"체류 데이터 필드가 부족합니다: {sorted(missing_stay_columns)}")
if missing_consumption_columns:
    raise RuntimeError(
        f"소비 데이터 필드가 부족합니다: {sorted(missing_consumption_columns)}"
    )

stay["value"] = pd.to_numeric(stay["tarSjrnDsIxVal"], errors="coerce")
consumption["value"] = pd.to_numeric(
    consumption["tarExpDsIxVal"], errors="coerce"
)

stay = stay.dropna(subset=["value"]).copy()
consumption = consumption.dropna(subset=["value"]).copy()

# signguNm이 '_'인 행은 서울 전체 값이므로 자치구 순위에서는 제외합니다.
stay_regions = stay[stay["signguNm"].astype(str).str.strip() != "_"].copy()
consumption_regions = consumption[
    consumption["signguNm"].astype(str).str.strip() != "_"
].copy()

stay_top10 = stay_regions.sort_values("value", ascending=False).head(10)
consumption_top10 = consumption_regions.sort_values("value", ascending=False).head(10)

if stay_top10.empty or consumption_top10.empty:
    raise RuntimeError("관광 지역별 분석 결과가 비어 있습니다.")

chart_data = consumption_top10.sort_values("value", ascending=True)
plt.figure(figsize=(10, 6))
plt.barh(chart_data["signguNm"], chart_data["value"], color="#4C78A8")
plt.title("관광 소비 강도 상위 지역")
plt.xlabel("관광 소비 강도")
plt.ylabel("지역")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig(TOURISM_CHART_PATH, dpi=150)
plt.close()


# 3. 핵심 결과를 하나의 요약 CSV로 저장
summary_rows = []

for row in latest_naver.itertuples(index=False):
    summary_rows.append(
        {
            "source": "NAVER",
            "period": row.period.strftime("%Y-%m-%d"),
            "item": row.keyword,
            "metric": "search_interest_ratio",
            "value": round(float(row.ratio), 4),
            "change_from_previous": (
                round(float(row.change_from_previous), 4)
                if pd.notna(row.change_from_previous)
                else None
            ),
        }
    )

for row in stay_top10.itertuples(index=False):
    summary_rows.append(
        {
            "source": "TOURISM",
            "period": str(row.baseYm),
            "item": row.signguNm,
            "metric": "stay_intensity",
            "value": round(float(row.value), 4),
            "change_from_previous": None,
        }
    )

for row in consumption_top10.itertuples(index=False):
    summary_rows.append(
        {
            "source": "TOURISM",
            "period": str(row.baseYm),
            "item": row.signguNm,
            "metric": "consumption_intensity",
            "value": round(float(row.value), 4),
            "change_from_previous": None,
        }
    )

summary = pd.DataFrame(summary_rows)
summary.to_csv(SUMMARY_PATH, index=False, encoding="utf-8-sig")

print("[PASS] Analysis")
print("NAVER latest:")
print(
    latest_naver[["period", "keyword", "ratio", "change_from_previous"]]
    .to_string(index=False)
)
print("stay top region:", stay_top10.iloc[0]["signguNm"], stay_top10.iloc[0]["value"])
print(
    "consumption top region:",
    consumption_top10.iloc[0]["signguNm"],
    consumption_top10.iloc[0]["value"],
)
print("saved:", NAVER_CHART_PATH)
print("saved:", TOURISM_CHART_PATH)
print("saved:", SUMMARY_PATH)
