# 수업 자료 비교 및 가져오기

비교일: 2026-10-01. 로컬 `ai-data-analysis`의 기존 작업 내용을 기준으로 비교했습니다.

| 원본 | 비교한 커밋 | 결과 |
| --- | --- | --- |
| [course-admin](https://github.com/sangjae-lee97/course-admin) | `a96a7548169c74d5367d3f1e345dffc516da0a71` | PHP/MySQL 수강 관리 앱 11개 파일 추가 |
| [kant-axagent-study](https://github.com/sangjae-lee97/kant-axagent-study) | `843f41397bb0403e00e90d95b98378b65ea8d49c` | 일반 추가 200개, 기존 파일과 다른 원본의 참고 사본 109개, 동일 파일 32개 확인 |

원본 374개 파일 중 320개를 가져왔습니다. 이 중 151개는 충돌 사본, 원본 과제 답안, 원본 설정 등을 담은 `references` 아래에 있습니다. 가져온 노트북은 34개입니다. 원래 있던 파일 351개의 내용은 보존했습니다. 기존에 수정 중이던 파일, 미추적 파일 및 `llm-data-analysis-stury` 폴더도 유지했습니다. 커밋과 푸시는 하지 않았습니다.

## 현재 구조에 맞춘 배치

| 원본 자료 | 현재 위치 | 용도 |
| --- | --- | --- |
| `python-basics` | [`01_python-basics`](../01_python-basics/) | 기존 장별 폴더에 누락 예제, 미션, 데이터 추가. 22장 폴더 추가 |
| DB `code/chapter05` | [`assignments/chapter05`](../00_llm-data-analysis-course/assignments/chapter05/) | 도서관 스키마·시드·검증 SQL |
| DB `code/chapter07~09` | 기존 `assignments/chapter07`, `chapter08_SQL`, `chapter09_SQL` | 동일 SQL은 생략하고 다른 버전은 참고 보관 |
| DB `code/chapter10` | [`assignments/chapter10_SQL`](../00_llm-data-analysis-course/assignments/chapter10_SQL/) | 성능 실습: 데이터 생성, EXPLAIN, 인덱스, 결과 검증 |
| DB 과제 답안·화면 | 각 `assignments/chapterXX/references/kant-axagent-study` | 다른 수강생의 제출 결과임을 구분한 참고 자료. DB 8~10장은 `chapterXX_SQL` 사용 |
| 분석 `chapter04` | 기존 `notebooks/chapter04` | 기존 작업과 비교하고 추가 자료 배치 |
| 분석 `chapter05`, `chapter08` | 기존 `assignments/chapter05`, `assignments/chapter08` | 추가 이미지 및 기존 노트북의 다른 버전 참고 보관 |
| 분석 `chapter01`, `chapter06`, `chapter07`, `chapter09`, `chapter10` | `practice/chapterXX` | 기존 실습 구조에 맞춘 자료 배치 |
| 분석 장별 보충 노트북 | `notebooks/ch04`, `ch05`, `ch10` 등 | 누락된 수업 노트북 추가. 기존 6~8장 노트북은 별칭 경로로 비교 |
| `notebooks/book-text-ml` | [`notebooks/book_test_ML`](../00_llm-data-analysis-course/notebooks/book_test_ML/) | 도서 분석 1·2·5장, TF-IDF, 오분류·예측·추천 결과 추가 |
| `notebooks/book-text-ml-improved` | [`notebooks/book_test_ML/improved`](../00_llm-data-analysis-course/notebooks/book_test_ML/improved/) | 개선 도서 분석 노트북, 앱, 데이터 |
| 분석 `src`, `scripts`, `reports`, `models` | 기존 분석 수업 폴더의 같은 하위 폴더 | 회귀·분류 코드, 준비/실행 스크립트, 원본 참고 보고서, 모델 자료 |
| `course-admin` | [`02_course-admin`](../02_course-admin/) | 별도 PHP/MySQL 앱. 실행 조건은 앱 README 참고 |

같은 경로에 다른 내용이 있으면 기존 파일을 덮어쓰지 않고 `00_llm-data-analysis-course/references/kant-axagent-study/<원본의 수업 내부 경로>` 또는 `01_python-basics/references/kant-axagent-study/<원본의 Python 내부 경로>`에 보관했습니다.

## 먼저 확인할 추가 수업

- [SQL 10장 성능 실습](../00_llm-data-analysis-course/assignments/chapter10_SQL/01_performance_lab_schema.sql)
- [분석 9장 회귀 노트북](../00_llm-data-analysis-course/practice/chapter09/chapter09.ipynb)
- [분석 10장 분류 노트북](../00_llm-data-analysis-course/practice/chapter10/chapter10.ipynb)
- [Python 22장 노트북](../01_python-basics/chapter22/00.ipynb)
- [도서 분석 개선 노트북](../00_llm-data-analysis-course/notebooks/book_test_ML/improved/00.ipynb)
- [PHP 수강 관리 앱 실행 안내](../02_course-admin/README.md)

## 경로 조정 및 실행

추가한 분석 노트북에는 현재 수업 루트를 찾고 `sys.path`를 설정하는 셀을 넣었습니다. 원본 작성자 PC의 절대 경로 및 이동으로 달라진 데이터 경로를 수정했습니다. 기존 `course_utils.paths.get_data_dir()`는 `data/raw`를 반환하지만 원본은 `data`를 반환하므로, 추가한 실행용 노트북에서는 `COURSE_ROOT / "data"`를 직접 사용합니다. 기존 공통 유틸리티는 변경하지 않았습니다.

PowerShell에서 분석 9·10장 스크립트 실행:

```powershell
Set-Location C:\dev\ai-data-analysis\00_llm-data-analysis-course
..\.venv\Scripts\python.exe scripts\prepare_ch09_data.py
..\.venv\Scripts\python.exe scripts\run_regression_analysis.py
..\.venv\Scripts\python.exe scripts\prepare_ch10_data.py
..\.venv\Scripts\python.exe scripts\run_classification_analysis.py
..\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

준비·분석 스크립트는 `data/processed`와 `reports`에 결과를 생성합니다. 위 명령은 사용자가 분석을 다시 실행할 때 사용하며, 가져오기 과정에서는 기존 결과에 쓰지 않았습니다. 노트북의 파일 이름만 쓰는 도서 CSV/XLSX 셀은 해당 노트북 폴더를 작업 디렉터리로 사용합니다.

`references` 자료는 원본 비교·읽기용입니다. 원본 경로, 이미지 링크, 공통 모듈 계약을 그대로 유지한 사본이 있으므로 그 위치에서 바로 실행된다고 검증하지 않았습니다. 원본의 답안, 노트북 출력, 보고서, 모델은 원본 작성자의 결과이며 내 데이터로 재실행한 결과가 아닙니다.

## 검증과 제외

- 가져온 비어 있지 않은 노트북 34개의 JSON 구조를 확인했습니다.
- 가져온 Python 소스의 문법을 확인했습니다. 원본 `python-basics/chapter03/03_01.py`의 미완성 `print(`는 참고 사본에 보존했습니다. `chapter07/mission03.py`에는 원본에서 의도적으로 만든 문법·인덱스·타입 오류 실습이 포함되어 있습니다.
- 현재 레포의 원본 데이터로 전처리 → 회귀 → 분류 파이프라인을 임시 폴더에서 실행했습니다. 관계 검증, 회귀 검증 6개, 분류 검증 7개 모두 통과했습니다. 기존 데이터·보고서는 덮어쓰지 않았습니다.
- PHP 실행기가 없어 PHP 앱 실행과 MySQL 연결은 검증하지 않았습니다. SQL은 파일을 가져왔으며 실제 DB에 실행하지 않았습니다. 전체 노트북과 저장된 모델의 실행은 검증하지 않았습니다.
- 원본의 빈 `chapter06/chapter06.ipynb`, `notebooks/ch09/00.ipynb`는 제외했습니다. 6장 자료는 기존 `notebooks/ch06.ipynb`, 9장 자료는 추가한 `practice/chapter09/chapter09.ipynb`를 사용합니다.
- 캐시, `.pyc`, `.egg-info`, `.vscode`, `.gitkeep` 등과 빈 노트북을 합쳐 22개 제외했습니다.
- 기존 `.gitignore`를 유지했습니다. 가져온 파일은 커밋하지 않은 로컬 추가 상태입니다.

전체 파일의 원본 경로, 원본 커밋, 현재 경로, 처리 사유, 원본/현재 SHA-256은 [가져오기 명세 CSV](course-materials-manifest.csv)에 기록했습니다.
