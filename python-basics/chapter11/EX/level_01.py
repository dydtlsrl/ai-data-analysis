# 레드, 블루 블랙 노랑 블루/노랑 레/그/블 블/노/검


colors = ["red", "green", "blue", "yellow", "black"]

# print(colors[0])
# print(colors[2])
# print(colors[-1])
# print(colors[-2])
# print(colors[1:4])
# print(colors[:3])
# print(colors[3:])

# 첫 인덱스가 0임을 설명할 수 있다.
print(colors[0])
#파이썬 리스트의 인덱스는 0부터 시작하므로 첫 번째 값이 'red' 로 출력된다.
#리스트의 첫 번째 값인 'red'를 인덱스 0으로 출력이 되었기 때문에,
#리스트의 인덱스는 0으로 시작하는 것을 알 수있다.


#[-1]로 마지막 값을 가져왔다.
print(colors[-1])


#슬라이싱 끝 인덱스가 포함되지 않음을 설명.
print(colors[1:4])
#앞서 설명했 듯 인덱스 번호 0번째 red, 1번째 green, 2번째 blue, 3번째 yellow, 4번째 black
#슬라이싱으로 1번째 부터 4번째로 슬라이싱 했을 때, 0번째 red와 4번째 black은 출력 되지 않음
#즉 슬라이싱에서 앞의 앞쪽 숫자는 출력에 포함, 뒷쪽 번호의 전번호 까지 출력됨을 알 수 있다.

#실행 전에 결과를 예상 할 수 있다.