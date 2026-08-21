member_name = input("너의 이름은:")
order_price = int(input("얼만치 살껀데?:"))
member_answer = input("회원인강(y/n):").strip().lower()

is_member = member_answer == "y"

if order_price >= 50000 or is_member == False :
    print("무료배송임")
else:
    print("배송비 3000원 있음")

    