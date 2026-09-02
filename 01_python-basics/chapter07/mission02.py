name=" 양성용"
city = "seoul"
lanquage = "Python"
intro = "I like Java"

a_name = name.split()
a_city = city.upper()
a_intro = intro.replace("Java","Python")

print(lanquage[0])
print(lanquage[-1])
print(len(lanquage))
print(f"이름:{a_name}\n사는곳:{a_city}\n한마디:{a_intro}")
print(f"lanquage의 첫 글자는 {lanquage[0]}이고 마지막 글자는 {lanquage[-1]}입니다.")
print(f"Python은 {len(lanquage)}입니다.")