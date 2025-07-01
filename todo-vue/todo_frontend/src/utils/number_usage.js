// 통화 형식
formatCurrency(10000); // '₩10,000'
formatCurrency(10000, 'en-US', 'USD'); // '$10,000'

// 천 단위 구분자
formatNumber(1000000); // '1,000,000'

// 파일 크기
formatFileSize(1024); // '1 KB'
formatFileSize(1048576); // '1 MB'

// 퍼센트
formatPercent(0.75); // '75%'
formatPercent(0.753, 1); // '75.3%'

// 반올림
roundNumber(3.14159, 2); // 3.14

// 범위 제한
clamp(150, 0, 100); // 100

// 랜덤 정수
randomInt(1, 10); // 1~10 사이의 랜덤 정수

// 한글 단위 변환
formatKoreanNumber(1234); // '천이백삼십사'
formatKoreanNumber(12345678); // '천이백삼십사만 오천육백칠십팔'