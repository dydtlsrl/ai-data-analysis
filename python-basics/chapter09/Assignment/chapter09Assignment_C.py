saved_id ="python"
saved_password = "1234"

login_id = input("ID를 입력하세요:")
login_pass = input("비밀번호 네자리(숫자)를 눌러주세요:")


if (login_id==saved_id) and (login_pass==saved_password):
    print("로그인 성공")
else:
    print("아이디 또는 비밀번호를 확인 하세요")