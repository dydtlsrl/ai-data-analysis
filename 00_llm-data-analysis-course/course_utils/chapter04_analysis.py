"""Chapter 04 매출 분석에서 반복하는 pandas 작업을 모은 함수들."""

from pathlib import Path

import pandas as pd


def load_raw_data(data_dir: Path) -> dict[str, pd.DataFrame]:
    """원본 CSV 4개를 읽어 테이블 이름별로 반환한다."""
    return {
        "customers": pd.read_csv(data_dir / "customers.csv", parse_dates=["signup_date"]),
        "orders": pd.read_csv(data_dir / "orders.csv", parse_dates=["order_date"]),
        "order_items": pd.read_csv(data_dir / "order_items.csv"),
        "products": pd.read_csv(data_dir / "products.csv"),
    }


def summarize_tables(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """테이블별 행 수, 열 수, 결측치 수를 한 표로 요약한다."""
    return pd.DataFrame(
        [
            {
                "table": name,
                "rows": len(table),
                "columns": len(table.columns),
                "missing_values": int(table.isna().sum().sum()),
            }
            for name, table in tables.items()
        ]
    )


def build_completed_sales(
    customers: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
    products: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """완료 주문의 상품 항목을 고객·상품 정보와 연결해 매출 분석용 표를 만든다."""
    completed_orders = orders.loc[
        orders["order_status"].eq("completed"),
        ["order_id", "customer_id", "order_date", "payment_method", "order_status"],
    ].copy()

    items_with_amount = order_items.copy()
    items_with_amount["line_total"] = (
        items_with_amount["quantity"] * items_with_amount["unit_price"]
    )

    sales = (
        items_with_amount.merge(
            completed_orders,
            on="order_id",
            how="inner",
            validate="many_to_one",
        )
        .merge(products, on="product_id", how="left", validate="many_to_one")
        .merge(
            customers[["customer_id", "name", "city"]],
            on="customer_id",
            how="left",
            validate="many_to_one",
        )
    )

    missing_products = sales.loc[
        sales["product_name"].isna(),
        ["order_id", "product_id", "quantity", "unit_price", "line_total"],
    ].copy()

    # 상품 마스터에 없는 값은 추측하지 않고 분석 결과에서만 미분류로 보존한다.
    sales["category"] = sales["category"].fillna("미분류")
    sales["product_name"] = sales["product_name"].fillna("상품 정보 없음")
    sales["order_month"] = sales["order_date"].dt.to_period("M").astype(str)

    return sales, missing_products


def make_revenue_reports(sales: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """하나의 매출 표에서 질문별 집계표 4개를 만든다."""
    return {
        "category_revenue": (
            sales.groupby("category", as_index=False)
            .agg(revenue=("line_total", "sum"), quantity=("quantity", "sum"))
            .sort_values("revenue", ascending=False)
        ),
        "product_revenue": (
            sales.groupby(
                ["product_id", "product_name", "category"], as_index=False
            )
            .agg(revenue=("line_total", "sum"), quantity=("quantity", "sum"))
            .sort_values("revenue", ascending=False)
        ),
        "monthly_revenue": (
            sales.groupby("order_month", as_index=False)
            .agg(revenue=("line_total", "sum"), order_count=("order_id", "nunique"))
            .sort_values("order_month")
        ),
        "customer_revenue": (
            sales.groupby(["customer_id", "name", "city"], as_index=False)
            .agg(revenue=("line_total", "sum"), order_count=("order_id", "nunique"))
            .sort_values("revenue", ascending=False)
        ),
    }


def validate_reports(sales: pd.DataFrame, reports: dict[str, pd.DataFrame]) -> int:
    """분석 기준과 모든 집계표의 총매출이 일치하는지 검증하고 총매출을 반환한다."""
    total_revenue = int(sales["line_total"].sum())

    assert sales["order_status"].eq("completed").all(), "완료되지 않은 주문이 포함되어 있습니다."
    assert sales["line_total"].ge(0).all(), "음수 매출 항목이 있습니다."

    for report_name, report in reports.items():
        report_total = int(report["revenue"].sum())
        assert total_revenue == report_total, (
            f"{report_name}의 매출 합계가 전체 매출과 다릅니다. "
            f"전체={total_revenue:,}, 집계={report_total:,}"
        )

    return total_revenue


def save_reports(reports: dict[str, pd.DataFrame], output_dir: Path) -> list[Path]:
    """집계표를 UTF-8-SIG CSV로 저장하고 저장 경로를 반환한다."""
    output_dir.mkdir(parents=True, exist_ok=True)
    saved_paths = []

    for report_name, report in reports.items():
        output_path = output_dir / f"{report_name}.csv"
        report.to_csv(output_path, index=False, encoding="utf-8-sig")
        saved_paths.append(output_path)

    return saved_paths
