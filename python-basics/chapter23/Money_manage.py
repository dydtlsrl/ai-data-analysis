# expense = {
#     "date" : "2026-09-01",
#     "category" : "전자기기",
#     "description" : "무선마우스",
#     "amount" : 21000,
#  }

import csv #표 형태의 데이터를 파일로 저장하는 간단한 형식




def add_expense(expenses):
    #정의한 함수(함수가 전달받을 매수변수)
    date = input("날짜(YYYY-MM-DD): ").strip()
    category = input("카테고리: ").strip()
    description = input("내용: ").strip()
    if not date or not category or not description:
        print("날짜, 카테고리, 내용은 비워 둘 수 없습니다.")
        return
    try:
        amount = int(input("금액: "))
    except ValueError:
        print("금액은 정수로 입력해 주세요.")
        return
    if amount <= 0:
        print("금액은 0보다 큰 값으로 입력해 주세요.")
        return

    expense = {
        "date": date,
        "category": category,
        "description": description,
        "amount": amount,
    }
    expenses.append(expense)



def show_expenses(expenses):
    if not expenses:
        print("등록된 지출이 없습니다.")
        return

    print("\n=== 지출 내역 ===")
    number = 1

    for expense in expenses:
        print(
            f"{number}. {expense['date']} | "
            f"{expense['category']} | "
            f"{expense['description']} | "
            f"{expense['amount']:,}원"
        )
        number += 1


def calculate_total(expenses):
    total = 0
    for expense in expenses:
        total += expense["amount"]
    return(total)


# add_expense(expenses)
# print(calculate_total(expenses))

def calculate_by_category(expenses):
    category_totals = {}
    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        if category not in category_totals:
            category_totals[category] = amount
        else:
            category_totals[category] += amount
    return(category_totals)

# add_expense(expenses)
# add_expense(expenses)
# add_expense(expenses)

# print(calculate_total(expenses))
# print(calculate_by_category(expenses))


def save_expenses(file_path, expenses):
    my_columns = ["date", "category", "description", "amount"]

    with open(file_path, "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=my_columns)

        writer.writeheader()
        writer.writerows(expenses)

# file_path = "python-basics/chapter23/없는파일.csv"
# save_expenses(file_path, expenses)


def load_expenses(file_path):
    expenses = []
    try:
        # print("읽는 파일:", file_path)

        with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
            reader =csv.DictReader(file)
            for row in reader:
                # print("읽은 행:", row)

                try:
                    row["amount"] = int(row["amount"])
                except ValueError:
                    print("잘 못 처리된 금액입니다.", row )
                    continue

                
                expenses.append(row)
    except FileNotFoundError :
        print("출력 가능한 데이터가 없습니다.")

    return expenses
            


# expenses = []

file_path = "python-basics/chapter23/expenses.csv"
expenses = load_expenses(file_path)


while True:
    print("\n=== 지출 관리 프로그램 ===")
    print("1. 지출 추가")
    print("2. 지출 목록")
    print("3. 목록 합계")
    print("4. 전체 합계")
    print("5. 저장")
    print("0. 종료")

    choice = input("선택: ").strip()
    if choice =="1":
        add_expense(expenses)
    elif choice =="2":
        show_expenses(expenses)
    elif choice =="3":
        print(calculate_by_category(expenses))
    elif choice =="4":
        print("총지출 금액:",calculate_total(expenses))
    elif choice =="5":
        save_expenses(file_path, expenses)
        print("저장했습니다.")
    elif choice == "0":
        break
    else:
        print("메뉴 번호를 다시 선택해주세요.")

# add_expense(expenses)
# save_expenses(file_path, expenses)
# print("총지출 금액:",calculate_total(expenses))
# print("카테고리별 지출:", calculate_by_category(expenses))
# show_expenses(expenses)
# print(expenses)