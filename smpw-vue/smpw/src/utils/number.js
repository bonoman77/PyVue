/**
 * 숫자 관련 유틸리티 함수
 */

/**
 * 숫자를 통화 형식으로 변환
 * @param {number} number - 변환할 숫자
 * @param {string} locale - 로케일 (기본값: 'ko-KR')
 * @param {string} currency - 통화 코드 (기본값: 'KRW')
 * @returns {string} 통화 형식의 문자열
 */
export function formatCurrency(number, locale = 'ko-KR', currency = 'KRW') {
  if (number === null || number === undefined || isNaN(number)) {
    return '';
  }
  
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(number);
}

/**
 * 숫자에 천 단위 구분자 추가
 * @param {number} number - 변환할 숫자
 * @param {string} locale - 로케일 (기본값: 'ko-KR')
 * @returns {string} 천 단위 구분자가 추가된 문자열
 */
export function formatNumber(number, locale = 'ko-KR') {
  if (number === null || number === undefined || isNaN(number)) {
    return '';
  }
  
  return new Intl.NumberFormat(locale).format(number);
}

/**
 * 파일 크기 포맷팅 (바이트를 KB, MB 등으로 변환)
 * @param {number} bytes - 바이트 단위 크기
 * @param {number} decimals - 소수점 자릿수 (기본값: 2)
 * @returns {string} 포맷팅된 파일 크기
 */
export function formatFileSize(bytes, decimals = 2) {
  if (bytes === 0) return '0 Bytes';
  if (bytes === null || bytes === undefined || isNaN(bytes)) return '';
  
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(decimals)) + ' ' + sizes[i];
}

/**
 * 숫자를 퍼센트 형식으로 변환
 * @param {number} number - 변환할 숫자 (0-1 사이의 값)
 * @param {number} decimals - 소수점 자릿수 (기본값: 0)
 * @returns {string} 퍼센트 형식의 문자열
 */
export function formatPercent(number, decimals = 0) {
  if (number === null || number === undefined || isNaN(number)) {
    return '';
  }
  
  return (number * 100).toFixed(decimals) + '%';
}

/**
 * 숫자를 지정된 자릿수로 반올림
 * @param {number} number - 반올림할 숫자
 * @param {number} decimals - 소수점 자릿수 (기본값: 0)
 * @returns {number} 반올림된 숫자
 */
export function roundNumber(number, decimals = 0) {
  if (number === null || number === undefined || isNaN(number)) {
    return 0;
  }
  
  return Number(Math.round(number + 'e' + decimals) + 'e-' + decimals);
}

/**
 * 숫자 범위 제한
 * @param {number} number - 제한할 숫자
 * @param {number} min - 최소값
 * @param {number} max - 최대값
 * @returns {number} 범위 내로 제한된 숫자
 */
export function clamp(number, min, max) {
  if (number === null || number === undefined || isNaN(number)) {
    return min;
  }
  
  return Math.min(Math.max(number, min), max);
}

/**
 * 랜덤 정수 생성
 * @param {number} min - 최소값 (포함)
 * @param {number} max - 최대값 (포함)
 * @returns {number} 생성된 랜덤 정수
 */
export function randomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * 숫자를 한글 단위로 변환 (예: 1000 -> 1천, 10000000 -> 1천만)
 * @param {number} number - 변환할 숫자
 * @returns {string} 한글 단위로 변환된 문자열
 */
export function formatKoreanNumber(number) {
  if (number === null || number === undefined || isNaN(number)) {
    return '';
  }
  
  const units = ['', '만', '억', '조', '경'];
  const digits = ['', '일', '이', '삼', '사', '오', '육', '칠', '팔', '구'];
  const tenUnits = ['', '십', '백', '천'];
  
  if (number === 0) return '영';
  if (number < 0) return '마이너스 ' + formatKoreanNumber(-number);
  
  let result = '';
  let unitIndex = 0;
  
  while (number > 0) {
    let segment = number % 10000;
    number = Math.floor(number / 10000);
    
    if (segment === 0) {
      unitIndex++;
      continue;
    }
    
    let segmentText = '';
    for (let i = 0; i < 4; i++) {
      const digit = segment % 10;
      segment = Math.floor(segment / 10);
      
      if (digit !== 0) {
        segmentText = (i > 0 && digit === 1 ? '' : digits[digit]) + tenUnits[i] + segmentText;
      }
    }
    
    result = segmentText + (unitIndex > 0 ? units[unitIndex] : '') + (result ? ' ' + result : '');
    unitIndex++;
  }
  
  return result;
}
