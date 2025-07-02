/**
 * 문자열 관련 유틸리티 함수
 */

/**
 * 문자열 자르기 (말줄임표 추가)
 * @param {string} str - 원본 문자열
 * @param {number} length - 최대 길이
 * @param {string} ellipsis - 말줄임표 문자열
 * @returns {string} 잘린 문자열
 */
export function truncate(str, length = 30, ellipsis = '...') {
  if (!str) return '';
  return str.length > length ? str.substring(0, length) + ellipsis : str;
}

/**
 * 특수문자 제거
 * @param {string} str - 원본 문자열
 * @returns {string} 특수문자가 제거된 문자열
 */
export function removeSpecialChars(str) {
  if (!str) return '';
  return str.replace(/[^\w\s가-힣]/gi, '');
}

/**
 * 문자열이 비어있는지 확인
 * @param {string} str - 확인할 문자열
 * @returns {boolean} 비어있으면 true, 아니면 false
 */
export function isEmpty(str) {
  return !str || str.trim() === '';
}

/**
 * 문자열 첫 글자를 대문자로 변환
 * @param {string} str - 원본 문자열
 * @returns {string} 첫 글자가 대문자인 문자열
 */
export function capitalize(str) {
  if (!str) return '';
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * 문자열 내 특정 문자열 모두 치환
 * @param {string} str - 원본 문자열
 * @param {string} search - 찾을 문자열
 * @param {string} replace - 대체할 문자열
 * @returns {string} 치환된 문자열
 */
export function replaceAll(str, search, replace) {
  if (!str) return '';
  return str.split(search).join(replace);
}

/**
 * HTML 태그 제거
 * @param {string} html - HTML 문자열
 * @returns {string} HTML 태그가 제거된 문자열
 */
export function stripHtml(html) {
  if (!html) return '';
  return html.replace(/<\/?[^>]+(>|$)/g, '');
}

/**
 * 문자열에서 URL 추출
 * @param {string} text - 원본 문자열
 * @returns {string[]} 추출된 URL 배열
 */
export function extractUrls(text) {
  if (!text) return [];
  const urlRegex = /(https?:\/\/[^\s]+)/g;
  return text.match(urlRegex) || [];
}

/**
 * 문자열에서 이메일 추출
 * @param {string} text - 원본 문자열
 * @returns {string[]} 추출된 이메일 배열
 */
export function extractEmails(text) {
  if (!text) return [];
  const emailRegex = /([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)/g;
  return text.match(emailRegex) || [];
}

/**
 * 랜덤 문자열 생성
 * @param {number} length - 생성할 문자열 길이
 * @returns {string} 생성된 랜덤 문자열
 */
export function generateRandomString(length = 10) {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}
