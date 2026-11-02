// 1. 함수 기본 실습 (매개변수와 반환값)
function greet(name) {
    return `안녕하세요, ${name}님! 환영합니다.`;
}

const greetingBox = document.getElementById('greeting-box');
const nameInput = document.getElementById('name-input');
const greetBtn = document.getElementById('greet-btn');

// 화면에 인사말 출력하기
function showGreeting(name) {
    const message = greet(name);
    console.log(message); // 콘솔창 확인용
    greetingBox.innerHTML = `<p><strong>${message}</strong></p>`;
}

showGreeting('김코딩'); // 처음 화면 표시

// 확인 버튼을 누르면 입력한 이름으로 인사말 변경
greetBtn.addEventListener('click', () => {
    const name = nameInput.value.trim();
    if (name === '') {
        greetingBox.innerHTML = '<p>이름을 입력해 주세요.</p>';
        return;
    }
    showGreeting(name);
});


// 2. 객체(Object)와 배열(Array) 데이터 구조
const users = [
    { id: 1, name: '김철수', age: 25, isActive: true },
    { id: 2, name: '이영희', age: 30, isActive: false },
    { id: 3, name: '박민수', age: 28, isActive: true },
    { id: 4, name: '최지우', age: 24, isActive: false }
];


// 3. map() 활용: 모든 회원의 정보를 HTML 문자열 배열로 변환
const userListEl = document.getElementById('user-list');
const userHtmls = users.map(user => {
    return `<li>이름: ${user.name} / 나이: ${user.age}세</li>`;
});
userListEl.innerHTML = userHtmls.join(''); // 배열을 하나의 문자열로 합쳐서 화면에 출력


// 4. filter() 활용: isActive가 true인 활성 회원만 골라내기
const activeUserListEl = document.getElementById('active-user-list');
const activeUsers = users.filter(user => user.isActive);

const activeUserHtmls = activeUsers.map(user => {
    return `<li>활성 회원 이름: ${user.name}</li>`;
});
activeUserListEl.innerHTML = activeUserHtmls.join('');
