dan = int(input("출력할 단을 입력하세요: "))

for number in range(1, 12):
    result = dan * number
    print(f"{dan} × {number} = {result}", end=" ")
    if result%2 == 0:
        print("짝수 결과 입니다.", end=" ")
        
    print()
        