#나만의 조건 판단 프로그램

#과제A. 연령 안내 프로그램

age = int(input("나이를 입력하세요:"))

if age >= 20:
    print("성인")
elif age <= 19  and age >=17:
    print("고등학생")
elif age <= 16 and age >= 14:
    print("중학생")
elif age <= 13 and age >=8:
    print("초등학생")
else:
    print("미취학")

    