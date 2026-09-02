order_amount=48000
is_member = True

if order_amount >= 50000 or is_member:
    print("무료배송입니다.")
else:
    print("배송비가 있습니다.")