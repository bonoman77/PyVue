// 날짜 포맷팅
formatDate(new Date(), 'YYYY년 MM월 DD일'); // '2025년 07월 01일'
formatDate('2025-07-01', 'MM/DD/YYYY'); // '07/01/2025'

// 날짜 차이 계산
dateDiff('2025-07-01', '2025-07-10'); // 9 (일)
dateDiff('2025-07-01 12:00', '2025-07-01 18:00', 'hours'); // 6 (시간)

// 상대적 시간
timeAgo('2025-06-30'); // '1일 전'
timeAgo('2025-06-01'); // '1개월 전'

// 상대 날짜 가져오기
const yesterday = getRelativeDate('yesterday'); // 어제 날짜