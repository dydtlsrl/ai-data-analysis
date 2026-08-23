delivery_price= int(input("배송비:"))
python_book=16500
quantity = int(input("구매수량:"))
total_price=python_book*quantity+delivery_price

print(f"파입썬 입문서: {python_book}원")
print(f"너는 파이썬입문서를 {quantity}개를 주문했습니다\n배송비 {delivery_price}원 포함, 총 {total_price}입니다.")