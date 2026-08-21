item_price = int(input("상품금액 입력:"))
t_sale = item_price * 0.1
f_sale = item_price * 0.05


if item_price >= 100000:
    print(f"할인 금액은 {t_sale}원 입니다.")
    print(f"결제하실 금액은 {item_price-t_sale}원 입니다.")
elif item_price >= 50000:
    print(f"할인 금액은 {f_sale}원 입니다.")
    print(f"결제하실 금액은 {item_price-f_sale}원 입니다.")
else:
    print("할인 금액은 없습니다.")

print("구매해 주셔서 감사합니다.")