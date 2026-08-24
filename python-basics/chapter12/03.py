tags = ["Python", "AI", "Python", "Data", "AI"]

result =[]

for i in range(len(tags)):
    if tags[i] not in result:
        result.append(tags[i])

print(result)

# *** AI에게 질문한 내용 ***
# 
# tags = ["Python", "AI", "Python", "Data", "AI"]
# 이것을 list 기능만 써서  set 메서드? 함수를 쓰지 않고 중복 값제거 후 나열 하기를 해야 되는데, 
# 우선 for문을 range(len(tags)) 로 시작 해서
# 하나씩 출력해 가면서 중복되는 값을 제외하고 다음 출력을 하면서 range를 돌아 끝내는 것으로 하려고 하는데,
# if 문으로 중복되는 range가 첫번째 돌 면서 첫번째로 중복 값이 있는지 체크
# 없으면 true로 값을 출력,다음 range로 넘어가고,
# 중복체크후 없으면 값출력, 아니면 다음으로 넘어가는 식의 논리를 생각했는데.




# print(type(tags))
# print(len(tags))

# unique_tage =set(tags)

# print(type(unique_tage))
# print(len(unique_tage))
# print(unique_tage)

#list 기능만 써서 unique_tags를 구현 하시오. set 쓰지 않고 중복 제거 후 나열하기.
#수도코드(의사코드) 로 작성해줘.

# tags.remove("Python")
# tags.remove("AI")
# print(tags)