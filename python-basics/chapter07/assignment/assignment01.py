name =" 용용이 "
email = "dydtlsrl@gmail.com"
city = "강북"
message = "I like Java"

clear_name = name.split()
clear_city = city.upper()
clear_message = message.replace("Java","Python")

print(email[0],email[-1])
print(len(email))


print(email[:3])
print(clear_name[0][0], clear_name[0][-1])
print(clear_message[:7])


print(f"이름:{clear_name}\n도시:{clear_city}\n이메일길이:{len(email)}")




#name.split() 시 변수 name은 문자열>>>리스트로 바뀌기 때문에
#원하는 위치의 글자를 반환 받을 때는 [n]-용용이,[n]-원하는 위치
# 으로 작성해야 한다.
#split() 만 공백을 정리하면서 리스트로 반환하는 것!