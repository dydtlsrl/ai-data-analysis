import json
import os

from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


# 1. 기본 경로 설정
BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw"
CONFIG_PATH = BASE_DIR / "config" / "tourism_params.json"

RAW_DIR.mkdir(parents=True, exist_ok=True)


# 2. 환경변수 불러오기
load_dotenv(BASE_DIR / ".env")

service_key = os.getenv("TOURISM_SERVICE_KEY")
stay_url = os.getenv("TOURISM_STAY_URL")
consumption_url = os.getenv("TOURISM_CONSUMPTION_URL")

if not service_key:
    raise RuntimeError("TOURISM_SERVICE_KEY가 없습니다.")

if not stay_url or not consumption_url:
    raise RuntimeError("관광 API URL이 설정되지 않았습니다.")


# 3. JSON 설정 파일 읽기
with CONFIG_PATH.open("r", encoding="utf-8") as f:
    config = json.load(f)


# 4. 관광 API 호출 함수
def call_api(name, url, params):

    request_params = dict(params)
    request_params["serviceKey"] = service_key

    print(f"\n[INFO] {name} API 요청 시작")

    # API 요청
    response = requests.get(
        url,
        params=request_params,
        timeout=30,
    )

    print(f"[INFO] HTTP 상태코드: {response.status_code}")

    # HTTP 오류 확인
    if response.status_code != 200:
        raise RuntimeError(
            f"{name} API 실패\n"
            f"HTTP 상태코드: {response.status_code}\n"
            f"서버 응답: {response.text[:500]}"
        )

    # JSON 변환
    try:
        data = response.json()

    except ValueError as e:
        raise RuntimeError(
            f"{name} 응답이 JSON이 아닙니다.\n"
            f"서버 응답: {response.text[:500]}"
        ) from e

    # 응답 데이터 확인
    if not data:
        raise RuntimeError(
            f"{name} 응답이 비어 있습니다."
        )

    # 공공데이터 API 결과 코드 확인
    result = data.get("response", {}).get("header", {})

    result_code = result.get("resultCode")
    result_msg = result.get("resultMsg")

    print(f"[INFO] API 결과코드: {result_code}")
    print(f"[INFO] API 결과메시지: {result_msg}")

    if result_code is not None and str(result_code).zfill(4) != "0000":
        raise RuntimeError(
            f"{name} API 응답 오류: {result_code} / {result_msg}"
        )

    return data


# 5. 관광 체류 강도 API 호출
stay_data = call_api(
    "stay",
    stay_url,
    config["stay"]["params"],
)


# 6. 관광 소비 강도 API 호출
consumption_data = call_api(
    "consumption",
    consumption_url,
    config["consumption"]["params"],
)


# 7. 저장 파일명 생성
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

stay_path = RAW_DIR / f"tourism_stay_{timestamp}.json"
consumption_path = RAW_DIR / f"tourism_consumption_{timestamp}.json"


# 8. 관광 체류 강도 JSON 저장
with stay_path.open("w", encoding="utf-8") as f:
    json.dump(
        stay_data,
        f,
        ensure_ascii=False,
        indent=2
    )


# 9. 관광 소비 강도 JSON 저장
with consumption_path.open("w", encoding="utf-8") as f:
    json.dump(
        consumption_data,
        f,
        ensure_ascii=False,
        indent=2
    )


# 10. 최종 실행 결과 출력
print("\n[PASS] Tourism API")
print("stay saved:", stay_path)
print("consumption saved:", consumption_path)