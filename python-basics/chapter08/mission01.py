customer = input("고객이름:").split()
product = input("상품명:").split()
price = int(input("상품가격:"))
quantity = int(input("수량:"))
total = price * quantity

# 고객이름 : 입력값
# 상품명 : 입력값
# 상품가격 : 입력값
# 수량 : 입력값
# total = 가격 * 수량

print(f"구매 수량은 {quantity}개 이고,")
print(f" 총 구매 금액은 {total}원 입니다.")
