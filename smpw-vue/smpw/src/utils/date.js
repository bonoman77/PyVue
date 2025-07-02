/**
 * 날짜 관련 유틸리티 함수
 */

/**
 * 날짜를 원하는 형식으로 변환
 * @param {Date|string} date - 변환할 날짜 (Date 객체 또는 날짜 문자열)
 * @param {string} format - 변환할 형식 (YYYY: 년, MM: 월, DD: 일, HH: 시, mm: 분, ss: 초)
 * @returns {string} 포맷팅된 날짜 문자열
 */
export function formatDate(date, format = 'YYYY-MM-DD') {
  // 문자열이면 Date 객체로 변환
  const dateObj = date instanceof Date ? date : new Date(date);
  
  // 유효하지 않은 날짜인 경우
  if (isNaN(dateObj.getTime())) {
    console.error('유효하지 않은 날짜입니다:', date);
    return '';
  }
  
  const year = dateObj.getFullYear();
  const month = String(dateObj.getMonth() + 1).padStart(2, '0');
  const day = String(dateObj.getDate()).padStart(2, '0');
  const hours = String(dateObj.getHours()).padStart(2, '0');
  const minutes = String(dateObj.getMinutes()).padStart(2, '0');
  const seconds = String(dateObj.getSeconds()).padStart(2, '0');
  
  // 포맷 문자열 치환
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
    .replace('HH', hours)
    .replace('mm', minutes)
    .replace('ss', seconds);
}

/**
 * 두 날짜 사이의 차이 계산
 * @param {Date|string} date1 - 첫 번째 날짜
 * @param {Date|string} date2 - 두 번째 날짜
 * @param {string} unit - 반환할 단위 ('days', 'hours', 'minutes', 'seconds')
 * @returns {number} 두 날짜 사이의 차이
 */
export function dateDiff(date1, date2, unit = 'days') {
  // 문자열이면 Date 객체로 변환
  const dateObj1 = date1 instanceof Date ? date1 : new Date(date1);
  const dateObj2 = date2 instanceof Date ? date2 : new Date(date2);
  
  // 유효하지 않은 날짜인 경우
  if (isNaN(dateObj1.getTime()) || isNaN(dateObj2.getTime())) {
    console.error('유효하지 않은 날짜입니다:', date1, date2);
    return 0;
  }
  
  // 밀리초 단위 차이
  const diffMs = Math.abs(dateObj2.getTime() - dateObj1.getTime());
  
  // 단위별 변환
  switch (unit.toLowerCase()) {
    case 'days':
      return Math.floor(diffMs / (1000 * 60 * 60 * 24));
    case 'hours':
      return Math.floor(diffMs / (1000 * 60 * 60));
    case 'minutes':
      return Math.floor(diffMs / (1000 * 60));
    case 'seconds':
      return Math.floor(diffMs / 1000);
    default:
      console.warn('지원하지 않는 단위입니다:', unit);
      return Math.floor(diffMs / (1000 * 60 * 60 * 24)); // 기본값: 일 단위
  }
}

/**
 * 날짜를 상대적 시간으로 표시 (예: "3일 전", "방금 전")
 * @param {Date|string} date - 변환할 날짜
 * @returns {string} 상대적 시간 문자열
 */
export function timeAgo(date) {
  const dateObj = date instanceof Date ? date : new Date(date);
  const now = new Date();
  
  // 유효하지 않은 날짜인 경우
  if (isNaN(dateObj.getTime())) {
    console.error('유효하지 않은 날짜입니다:', date);
    return '';
  }
  
  const diffSeconds = Math.floor((now - dateObj) / 1000);
  
  // 미래 날짜인 경우
  if (diffSeconds < 0) {
    return '미래';
  }
  
  // 시간대별 표시
  if (diffSeconds < 60) {
    return '방금 전';
  } else if (diffSeconds < 3600) {
    return `${Math.floor(diffSeconds / 60)}분 전`;
  } else if (diffSeconds < 86400) {
    return `${Math.floor(diffSeconds / 3600)}시간 전`;
  } else if (diffSeconds < 604800) {
    return `${Math.floor(diffSeconds / 86400)}일 전`;
  } else if (diffSeconds < 2592000) {
    return `${Math.floor(diffSeconds / 604800)}주 전`;
  } else if (diffSeconds < 31536000) {
    return `${Math.floor(diffSeconds / 2592000)}개월 전`;
  } else {
    return `${Math.floor(diffSeconds / 31536000)}년 전`;
  }
}

/**
 * 오늘, 내일, 어제 날짜 가져오기
 * @param {string} when - 'today', 'tomorrow', 'yesterday' 중 하나
 * @returns {Date} 해당하는 날짜 객체
 */
export function getRelativeDate(when = 'today') {
  const today = new Date();
  
  switch (when.toLowerCase()) {
    case 'yesterday':
      today.setDate(today.getDate() - 1);
      break;
    case 'tomorrow':
      today.setDate(today.getDate() + 1);
      break;
    case 'today':
    default:
      // 오늘은 기본값이므로 변경 없음
      break;
  }
  
  return today;
}