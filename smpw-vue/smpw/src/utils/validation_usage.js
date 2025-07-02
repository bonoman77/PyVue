// 기본 검증
isValidEmail('user@example.com'); // true
isValidPhone('010-1234-5678'); // true
isValidUrl('https://example.com'); // true

// 비밀번호 강도 검사
const strength = checkPasswordStrength('Abc123!@');
console.log(strength.score); // 5
console.log(strength.strengthText); // '매우 강함'
console.log(strength.feedback); // ['좋은 비밀번호입니다.']

// 폼 검증
const formData = {
  username: '홍길동',
  email: 'user@example.com',
  password: 'weakpw'
};

const rules = {
  username: ['required'],
  email: ['required', 'email'],
  password: ['required', { minLength: 8 }]
};

const result = validateForm(formData, rules);
console.log(result.isValid); // false
console.log(result.errors); // { password: '최소 8자 이상 입력해주세요.' }