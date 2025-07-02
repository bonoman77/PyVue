// 문자열 자르기
truncate('이것은 매우 긴 문자열입니다', 10); // '이것은 매우 ...'

// 특수문자 제거
removeSpecialChars('안녕하세요! 특수문자@#$를 제거합니다.'); // '안녕하세요 특수문자를 제거합니다'

// 빈 문자열 확인
isEmpty(''); // true
isEmpty('  '); // true
isEmpty('안녕'); // false

// 첫 글자 대문자화
capitalize('hello'); // 'Hello'

// HTML 태그 제거
stripHtml('<p>HTML <strong>태그</strong>를 제거합니다</p>'); // 'HTML 태그를 제거합니다'

// URL 추출
extractUrls('웹사이트는 https://example.com 입니다'); // ['https://example.com']

// 이메일 추출
extractEmails('연락처: user@example.com, admin@test.com'); // ['user@example.com', 'admin@test.com']

// 랜덤 문자열 생성
generateRandomString(8); // 'a1b2c3d4'