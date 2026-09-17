# Chapter 08 답안 양식. 작은 데이터 분석 프로젝트 완성하기

> 이 내용은 `chapter08.ipynb`의 Markdown 셀에도 같은 기준으로 작성했습니다.

## 제출 정보
- 이름: 양성용
- GitHub ID: dydtlsrl
- 작성일: 2026.09.17
- 최종 Notebook URL: https://github.com/dydtlsrl/ai-data-analysis/blob/main/00_llm-data-analysis-course/assignments/chapter08/chapter08.ipynb

## 1. 프로젝트 질문
### 분석 질문
1. completed 주문 기준으로 가장 큰 매출을 만든 상품 카테고리는 무엇인가?
2. completed 주문 금액은 월별로 어떻게 변하는가?
3. completed 주문 기준 구매 금액 상위 고객은 누구인가?

### 분석 범위
온라인 쇼핑몰의 고객·상품·주문·주문상세 데이터를 사용하되, 금액성 분석은 `order_status == "completed"`인 주문만 대상으로 한다.

### 사용할 데이터와 지표
- 데이터: `customers.csv`, `products.csv`, `orders.csv`, `order_items.csv`
- 지표: `line_total`, 카테고리별 매출, 월별 매출·주문 수, 고객별 구매 금액·주문 수

### 계산 기준
- `order_status == "completed"` 적용 여부: 적용했다. completed 주문 상세 474건을 금액성 분석에 사용했다.
- `line_total = quantity × unit_price` 확인 여부: 764건 전체에서 불일치 0건으로 확인했다.

### 완료 기준
PK/FK와 병합 검증을 통과하고, 카테고리·월별·고객별 집계의 총합이 completed source total과 일치하며, 개인정보 검증과 최종 Validation이 모두 PASS인 것을 완료 기준으로 삼았다.

## 2. 입력 데이터와 전처리 검증
- 사용 원본 파일: `customers.csv`, `products.csv`, `orders.csv`, `order_items.csv`
- shape: customers 150행 6열, products 100행 4열, orders 300행 5열, order_items 764행 5열
- 핵심 결측/중복 결과: 네 데이터셋 모두 결측값 0개, 중복 행 0개였다.
- 전처리 전후 변화: 모든 데이터셋의 행 수는 유지되었다. orders에는 `order_year`, `order_month`가 추가되어 5열에서 7열이 되었고, order_items에는 `line_total`이 추가되어 5열에서 6열이 되었다.

![입력 데이터 검증](images/step02_data_validation.png)

### 나의 해석과 판단
원본 행을 제거하지 않고 날짜·금액 파생 정보를 추가했으므로, 이후 분석의 관측 건수는 원본과 동일하게 유지된다.

### 한계와 추가 확인 사항
결측과 중복이 없다는 사실만으로 관계 무결성이나 금액 계산이 보장되지는 않는다. 따라서 PK/FK, 병합, `line_total`, 날짜 검증을 추가로 수행했다.

## 3. PK/FK·병합 검증
### PK 결과
- 결측: customers.customer_id, products.product_id, orders.order_id, order_items.order_item_id 모두 0건
- 중복: 네 PK 모두 0건
- PASS/FAIL: PASS

### FK 결과
- 미매칭: orders.customer_id → customers.customer_id, order_items.order_id → orders.order_id, order_items.product_id → products.product_id 모두 0건
- PASS/FAIL: PASS

### 병합 결과
- validate 관계: order_id → orders는 `many_to_one`, product_id → products는 `many_to_one`, customer_id → customers는 `one_to_one`
- 병합 전 행 수: 각각 764행, 474행, 100행
- 병합 후 행 수: 각각 764행, 474행, 100행으로 모두 유지
- 미매칭: 모두 0건
- PASS/FAIL: PASS

### 나의 해석과 판단
PK와 FK가 모두 유효하고 병합 전후 행 수도 보존되었다. 따라서 주문상세를 주문·상품·고객 정보와 연결하는 이후 집계의 기본 관계는 검증되었다.

## 4. 핵심 EDA 결과
### 결과 1
- 수치/표: 카테고리별 completed 주문 기준 매출은 스포츠 31,743,000원(21.31%), 전자기기 26,400,000원(17.72%), 생활용품 23,915,000원(16.05%) 순이다.
- 결과 관찰: 스포츠가 가장 높은 매출과 매출 비중을 보였다.
- 나의 해석과 판단: 이 기간의 completed 주문 매출 기준으로 스포츠 카테고리의 규모가 가장 컸다.
- 업무·분석적 의미: 스포츠 카테고리는 재고·프로모션·상품 구성 점검의 우선 후보가 될 수 있다.
- 한계: 매출 규모만으로 수익성, 재고 수준, 할인율, 반품률을 판단할 수 없다.

### 결과 2
- 수치/표: 월별 매출은 2025-10에 25,766,000원(26건)으로 가장 높고, 2026-07에 2,188,000원(2건)으로 가장 낮았다.
- 결과 관찰: 월별 금액과 주문 수가 기간에 따라 달라진다.
- 나의 해석과 판단: 특정 월의 매출 차이는 관찰되지만, 현재 데이터만으로 계절성이나 캠페인의 효과라고 단정할 수 없다.
- 업무·분석적 의미: 고매출·저매출 월을 후속 점검 대상으로 선정할 수 있다.
- 한계: 월별 기간이 완전한지, 프로모션·재고·반품이 어떤 영향을 주었는지는 데이터에 없다.

### 결과 3
- 수치/표: 고객별 구매 금액 상위 3명은 Customer 01 4,100,000원(5건), Customer 02 3,996,000원(4건), Customer 03 3,880,000원(4건)이다.
- 결과 관찰: 상위 고객의 구매 금액과 주문 수를 익명 라벨로 확인할 수 있다.
- 나의 해석과 판단: 상위 고객은 후속 분석의 후보가 될 수 있으나, 구매 금액만으로 충성도나 고객 가치를 확정하지 않는다.
- 업무·분석적 의미: 재구매, 상품 조합, 고객 세그먼트 분석을 위한 출발점으로 활용할 수 있다.
- 한계: 공개 결과에는 직접 식별정보와 원본 ID를 포함하지 않았으며, 고객 특성·마케팅 접점 데이터도 없다.

## 5. Total consistency와 날짜 검증
- completed source total: 148,990,000원
- category total: 148,990,000원
- monthly total: 148,990,000원
- customer total: 148,990,000원
- 총합 일치 여부: 네 총합이 모두 source total과 일치하여 PASS
- completed 주문 날짜 오류 건수: 0건
- 날짜 오류 영향 금액: 0원

### 불일치가 있었다면 원인
이번 실행에서는 불일치가 없었다. 불일치가 발생했다면 completed 범위 적용 누락, 병합으로 인한 행 증식, 집계 키 차이, `line_total` 계산 오류를 우선 확인했을 것이다.

## 6. 대표 시각화
![대표 그래프 1](images/graph01.png)
![대표 그래프 2](images/graph02.png)

### 그래프 선택 이유
월별 선 그래프는 시간에 따른 금액 변화를, 카테고리별 막대그래프는 항목 간 매출 규모를 비교하기에 적합하다. 두 그래프는 시간적 변화와 구성 차이를 함께 보여 준다.

### 그래프와 원본 집계값 일치 여부
일치한다. 그래프는 각각 `ch08_monthly_sales.csv`, `ch08_category_sales.csv`의 completed 주문 기준 집계값으로 생성했고, 각 집계의 총합은 source total 148,990,000원과 일치한다.

### 그래프에서 직접 관찰한 사실
월별 그래프에서 2025-10 매출이 가장 높고 2026-07 매출이 가장 낮다. 카테고리 그래프에서는 스포츠 매출이 가장 높고 패션 매출이 가장 낮다.

### 그래프만으로 말할 수 없는 것
그래프만으로 매출 변화의 원인, 수익성, 고객 만족도, 향후 매출을 말할 수 없다.

## 7. 개인정보 검증
- 공개 고객 CSV 컬럼: `customer_label`, `city`, `order_count`, `total_sales`, `avg_order_value`
- 원본 `customer_id` 포함 여부: 포함하지 않음
- 이름/이메일/전화번호/주소 포함 여부: 포함하지 않음
- 익명 라벨 방식: 원본 ID 대신 `Customer 01`과 같은 `customer_label`을 사용함
- PASS/FAIL: PASS

### 나의 판단
고객별 집계의 분석적 활용성은 유지하면서 원본 customer_id와 직접 식별정보를 공개 결과에서 제외했다. 다만 city도 상황에 따라 재식별 위험을 높일 수 있으므로 외부 공개 범위는 별도로 검토해야 한다.

## 8. 최종 Validation
`reports/ch08_project_validation.csv`의 결과를 요약한다.

| 검증 항목 | 결과 | 내가 확인한 근거 |
| --- | --- | --- |
| pk_integrity | PASS | 네 PK의 결측·중복이 모두 0건 |
| fk_integrity | PASS | 세 FK 관계의 미매칭이 모두 0건 |
| merge_checks_pass | PASS | 세 병합의 행 수 보존·미매칭 0건 |
| line_total_consistency | PASS | `quantity × unit_price` 불일치 0건 |
| completed_total_consistency | PASS | source/category/monthly/customer 총합이 모두 일치 |
| category_sales_ratio_pct_sum | PASS | 카테고리 매출 비중 합계 100.0% |
| completed_rows_with_invalid_order_date | PASS | 오류 0건, 영향 금액 0원 |
| public_customer_columns_safe | PASS | 금지 컬럼이 공개 고객 CSV에 없음 |

### FAIL이 있었다면 수정 내용
이번 실행에서는 모든 검증이 PASS였다. 따라서 데이터를 임의로 수정하지 않았고, 각 검증 결과를 Evidence 파일로 남겼다.

## 9. LLM 활용 기록
- 사용 여부: 사용함
- 사용 목적: 분석 결과의 과도한 해석 위험, 계산 기준의 누락 여부, 추가 검증 후보를 점검하는 보조 도구로 사용함
- Safe Context: 원본 고객 행이나 customer_id 대신 비식별 검증 결과와 집계 결과만 제공함
- Prompt 요약: `line_total = quantity × unit_price`, completed 범위, PK/FK·병합·총합·날짜·개인정보 검증 결과를 제시하고 분석 위험·과도한 표현·추가 검증을 검토하도록 요청함
- 제안 요약: 반품·취소·기간 누락·이상치와 같은 미확인 위험을 구분하고, 매출만으로 고객 충성도·캠페인 효과·원인을 단정하지 말 것을 제안함
- 반영/수정/보류: 계산 기준과 한계를 보고서에 명시했다. 데이터에 없는 원인·효과에 대한 추정은 보류했다.
- 사람이 검증한 근거: `ch08_project_validation.csv`, `ch08_total_consistency_check.csv`, 원본 집계 CSV와 Notebook 출력으로 모든 핵심 수치를 직접 대조했다.

## 10. 프로젝트 재현 확인
- `python scripts/run_midterm_project.py` 실행 여부: 실행함
- 재실행 결과: 전체 Evidence 파일이 생성되었고 최종 산출물 검증이 PASS였다.
- Notebook과 핵심 수치 일치 여부: completed source total 148,990,000원 및 category/month/customer 총합이 일치한다.
- 생성된 핵심 Evidence 파일 확인 여부: `ch08_total_consistency_check.csv`, `ch08_project_validation.csv`, 카테고리·월별·고객별 집계 CSV와 그래프 파일을 확인했다.

![재실행 결과](images/step06_reproduce.png)

### 나의 해석과 판단
재실행 가능한 프로젝트는 동일한 원본과 코드에서 같은 결과를 다시 확인할 수 있게 한다. 수동 계산이나 일회성 화면 결과에 의존하지 않아, 수정 후에도 검증·보고서·그래프를 일관되게 갱신할 수 있다.

## 11. 최종 프로젝트 요약
### 핵심 인사이트 3개
1. completed 주문 기준 총매출은 148,990,000원이며, 스포츠가 31,743,000원(21.31%)으로 가장 큰 카테고리였다.
2. 월별 매출은 2025-10에 25,766,000원으로 가장 높고 2026-07에 2,188,000원으로 가장 낮았다.
3. 익명 고객 기준 상위 구매자는 Customer 01(4,100,000원), Customer 02(3,996,000원), Customer 03(3,880,000원)이었다.

### 가장 중요한 업무·분석적 의미
검증된 completed 주문 데이터를 기준으로 카테고리·월별·고객별 매출을 같은 총합으로 연결했다. 따라서 운영 우선순위를 정하기 위한 신뢰 가능한 기초 지표를 제공한다.

### 현재 분석의 한계
반품·취소 사유, 원가·마진, 할인·프로모션, 재고, 고객 유입 경로가 없으므로 매출 차이의 원인이나 수익성을 판단할 수 없다. 또한 제한된 기간의 데이터이므로 장기 추세나 계절성을 확정할 수 없다.

### 다음 분석 제안
1. 반품·취소·환불 데이터와 원가를 추가해 순매출 및 마진 기준으로 재분석한다.
2. 프로모션·재고·유입 경로를 결합해 월별 매출 차이의 가능한 요인을 검증한다.
3. 익명 고객 단위의 재구매 주기·상품 조합·세그먼트 분석을 수행한다.

## 최종 체크
- [x] 질문과 지표가 연결됩니다.
- [x] 원본 데이터에서 다시 시작했습니다.
- [x] PK/FK·병합 검증 근거가 있습니다.
- [x] `line_total` 계산 관계를 확인했습니다.
- [x] 금액성 분석은 completed 범위를 사용했습니다.
- [x] category/month/customer 총합이 source total과 일치합니다.
- [x] 날짜 오류를 확인했습니다.
- [x] 공개 고객 결과에서 원본 ID와 직접 식별정보를 제거했습니다.
- [x] 대표 그래프와 원본 집계값을 비교했습니다.
- [x] 원인 과대 해석이 없습니다.
- [x] 최종 Validation이 모두 PASS입니다.
- [x] 전체 프로젝트를 재실행했습니다.
- [x] 한계와 다음 분석을 작성했습니다.
- [x] 최종 Notebook URL을 제출합니다.
