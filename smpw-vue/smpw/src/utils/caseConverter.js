/**
 * 스네이크 케이스 문자열을 카멜 케이스로 변환합니다.
 * @param {string} str - 변환할 스네이크 케이스 문자열
 * @returns {string} 카멜 케이스로 변환된 문자열
 */
export const snakeToCamel = (str) => {
  // 언더스코어로 시작하는 경우 처리
  if (str.startsWith('_')) {
    return '_' + str.substring(1).replace(/_([a-z])/g, (match, group) => group.toUpperCase());
  }
  return str.replace(/_([a-z])/g, (match, group) => group.toUpperCase());
};

/**
 * 카멜 케이스 문자열을 스네이크 케이스로 변환합니다.
 * @param {string} str - 변환할 카멜 케이스 문자열
 * @returns {string} 스네이크 케이스로 변환된 문자열
 */
export const camelToSnake = (str) => {
  // 첫 글자가 대문자인 경우 처리
  return str
    .replace(/^([A-Z])/, (match) => match.toLowerCase())
    .replace(/([A-Z])/g, (letter) => `_${letter.toLowerCase()}`);
};

/**
 * 객체의 모든 키를 스네이크 케이스에서 카멜 케이스로 변환합니다.
 * @param {Object} obj - 변환할 객체
 * @returns {Object} 키가 카멜 케이스로 변환된 새 객체
 */
export const convertObjectKeysToCamelCase = (obj) => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => convertObjectKeysToCamelCase(item));
  }

  const camelCaseObj = {};
  
  Object.keys(obj).forEach(key => {
    const camelKey = snakeToCamel(key);
    camelCaseObj[camelKey] = convertObjectKeysToCamelCase(obj[key]);
  });
  
  return camelCaseObj;
};

/**
 * 객체의 모든 키를 카멜 케이스에서 스네이크 케이스로 변환합니다.
 * @param {Object} obj - 변환할 객체
 * @returns {Object} 키가 스네이크 케이스로 변환된 새 객체
 */
export const convertObjectKeysToSnakeCase = (obj) => {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => convertObjectKeysToSnakeCase(item));
  }

  const snakeCaseObj = {};
  
  Object.keys(obj).forEach(key => {
    const snakeKey = camelToSnake(key);
    snakeCaseObj[snakeKey] = convertObjectKeysToSnakeCase(obj[key]);
  });
  
  return snakeCaseObj;
};
