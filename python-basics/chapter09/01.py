#temperature=20
temperature = int(input("기온:"))

if temperature >=30:
    print("오늘 날씨는 덥습니다")

if temperature <=30:
    print("오늘은 선선합니다")

print("오늘 날씨는 이래요")


#score =59

score = int(input("숫장:"))

print(f"{score}는 60보다 크거나 같은가? : {score >= 60}")