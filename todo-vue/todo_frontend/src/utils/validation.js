/**
 * 유효성 검사 관련 유틸리티 함수
 */

/**
 * 이메일 유효성 검사
 * @param {string} email - 검사할 이메일 주소
 * @returns {boolean} 유효한 이메일이면 true, 아니면 false
 */
export function isValidEmail(email) {
  if (!email) return false;
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

/**
 * 비밀번호 강도 검사
 * @param {string} password - 검사할 비밀번호
 * @returns {Object} 비밀번호 강도 정보 (점수, 피드백)
 */
export function checkPasswordStrength(password) {
  if (!password) {
    return { score: 0, feedback: '비밀번호를 입력해주세요.' };
  }

  let score = 0;
  const feedback = [];

  // 길이 검사
  if (password.length < 8) {
    feedback.push('비밀번호는 8자 이상이어야 합니다.');
  } else {
    score += 1;
  }

  // 대문자 포함 여부
  if (!/[A-Z]/.test(password)) {
    feedback.push('대문자를 포함해주세요.');
  } else {
    score += 1;
  }

  // 소문자 포함 여부
  if (!/[a-z]/.test(password)) {
    feedback.push('소문자를 포함해주세요.');
  } else {
    score += 1;
  }

  // 숫자 포함 여부
  if (!/[0-9]/.test(password)) {
    feedback.push('숫자를 포함해주세요.');
  } else {
    score += 1;
  }

  // 특수문자 포함 여부
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    feedback.push('특수문자를 포함해주세요.');
  } else {
    score += 1;
  }

  // 점수에 따른 피드백
  let strengthText = '';
  if (score < 2) {
    strengthText = '매우 약함';
  } else if (score < 3) {
    strengthText = '약함';
  } else if (score < 4) {
    strengthText = '보통';
  } else if (score < 5) {
    strengthText = '강함';
  } else {
    strengthText = '매우 강함';
  }

  return {
    score,
    strengthText,
    feedback: feedback.length > 0 ? feedback : ['좋은 비밀번호입니다.']
  };
}

/**
 * 전화번호 유효성 검사 (한국 번호 형식)
 * @param {string} phone - 검사할 전화번호
 * @returns {boolean} 유효한 전화번호이면 true, 아니면 false
 */
export function isValidPhone(phone) {
  if (!phone) return false;
  
  // 숫자만 추출
  const numbers = phone.replace(/[^0-9]/g, '');
  
  // 한국 전화번호 패턴 검사 (01X-XXXX-XXXX 또는 02-XXXX-XXXX 등)
  if (numbers.length === 11 && numbers.startsWith('010')) {
    return true;
  }
  
  if ((numbers.length === 10 && (numbers.startsWith('010') || numbers.startsWith('011') || 
      numbers.startsWith('016') || numbers.startsWith('017') || numbers.startsWith('018') || 
      numbers.startsWith('019')))) {
    return true;
  }
  
  if ((numbers.length === 9 || numbers.length === 10) && 
      (numbers.startsWith('02') || numbers.startsWith('03') || numbers.startsWith('04') || 
       numbers.startsWith('05') || numbers.startsWith('06'))) {
    return true;
  }
  
  return false;
}

/**
 * URL 유효성 검사
 * @param {string} url - 검사할 URL
 * @returns {boolean} 유효한 URL이면 true, 아니면 false
 */
export function isValidUrl(url) {
  if (!url) return false;
  
  try {
    new URL(url);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * 주민등록번호 유효성 검사
 * @param {string} rrn - 검사할 주민등록번호 (예: 123456-1234567)
 * @returns {boolean} 유효한 주민등록번호이면 true, 아니면 false
 */
export function isValidRRN(rrn) {
  if (!rrn) return false;
  
  // 숫자와 하이픈만 허용
  if (!/^\d{6}-\d{7}$/.test(rrn)) {
    return false;
  }
  
  const numbers = rrn.replace('-', '');
  
  // 주민등록번호 검증 알고리즘
  const multipliers = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5];
  let sum = 0;
  
  for (let i = 0; i < 12; i++) {
    sum += parseInt(numbers.charAt(i)) * multipliers[i];
  }
  
  const remainder = (11 - (sum % 11)) % 10;
  return remainder === parseInt(numbers.charAt(12));
}

/**
 * 사업자등록번호 유효성 검사
 * @param {string} brn - 검사할 사업자등록번호 (예: 123-45-67890)
 * @returns {boolean} 유효한 사업자등록번호이면 true, 아니면 false
 */
export function isValidBusinessNumber(brn) {
  if (!brn) return false;
  
  // 숫자와 하이픈만 허용
  if (!/^\d{3}-\d{2}-\d{5}$/.test(brn)) {
    return false;
  }
  
  const numbers = brn.replace(/-/g, '');
  
  // 사업자등록번호 검증 알고리즘
  const multipliers = [1, 3, 7, 1, 3, 7, 1, 3, 5];
  let sum = 0;
  
  for (let i = 0; i < 9; i++) {
    sum += parseInt(numbers.charAt(i)) * multipliers[i];
  }
  
  sum += parseInt(numbers.charAt(8)) * 5 / 10;
  
  const remainder = sum % 10;
  return (10 - remainder) % 10 === parseInt(numbers.charAt(9));
}

/**
 * 신용카드 번호 유효성 검사 (Luhn 알고리즘)
 * @param {string} cardNumber - 검사할 신용카드 번호
 * @returns {boolean} 유효한 신용카드 번호이면 true, 아니면 false
 */
export function isValidCreditCard(cardNumber) {
  if (!cardNumber) return false;
  
  // 숫자와 공백만 허용
  const numbers = cardNumber.replace(/\s+/g, '');
  
  if (!/^\d+$/.test(numbers) || numbers.length < 13 || numbers.length > 19) {
    return false;
  }
  
  // Luhn 알고리즘
  let sum = 0;
  let alternate = false;
  
  for (let i = numbers.length - 1; i >= 0; i--) {
    let n = parseInt(numbers.charAt(i));
    
    if (alternate) {
      n *= 2;
      if (n > 9) {
        n = (n % 10) + 1;
      }
    }
    
    sum += n;
    alternate = !alternate;
  }
  
  return sum % 10 === 0;
}

/**
 * 날짜 유효성 검사
 * @param {string} dateStr - 검사할 날짜 문자열 (YYYY-MM-DD 형식)
 * @returns {boolean} 유효한 날짜이면 true, 아니면 false
 */
export function isValidDate(dateStr) {
  if (!dateStr) return false;
  
  // YYYY-MM-DD 형식 검사
  if (!/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) {
    return false;
  }
  
  const parts = dateStr.split('-');
  const year = parseInt(parts[0]);
  const month = parseInt(parts[1]);
  const day = parseInt(parts[2]);
  
  // 월 범위 검사
  if (month < 1 || month > 12) {
    return false;
  }
  
  // 일 범위 검사
  const daysInMonth = new Date(year, month, 0).getDate();
  if (day < 1 || day > daysInMonth) {
    return false;
  }
  
  return true;
}

/**
 * 폼 필드 유효성 검사
 * @param {Object} fields - 검사할 필드 객체 {필드명: 값}
 * @param {Object} rules - 검사 규칙 객체 {필드명: [규칙1, 규칙2, ...]}
 * @returns {Object} 유효성 검사 결과 {isValid: boolean, errors: {필드명: 에러메시지}}
 */
export function validateForm(fields, rules) {
  const errors = {};
  let isValid = true;
  
  for (const field in rules) {
    if (rules.hasOwnProperty(field)) {
      const fieldRules = rules[field];
      const value = fields[field];
      
      for (const rule of fieldRules) {
        // 필수 입력 검사
        if (rule === 'required' && (!value || value.trim() === '')) {
          errors[field] = '필수 입력 항목입니다.';
          isValid = false;
          break;
        }
        
        // 이메일 검사
        if (rule === 'email' && value && !isValidEmail(value)) {
          errors[field] = '유효한 이메일 주소를 입력해주세요.';
          isValid = false;
          break;
        }
        
        // 전화번호 검사
        if (rule === 'phone' && value && !isValidPhone(value)) {
          errors[field] = '유효한 전화번호를 입력해주세요.';
          isValid = false;
          break;
        }
        
        // URL 검사
        if (rule === 'url' && value && !isValidUrl(value)) {
          errors[field] = '유효한 URL을 입력해주세요.';
          isValid = false;
          break;
        }
        
        // 날짜 검사
        if (rule === 'date' && value && !isValidDate(value)) {
          errors[field] = '유효한 날짜를 입력해주세요. (YYYY-MM-DD)';
          isValid = false;
          break;
        }
        
        // 최소 길이 검사
        if (typeof rule === 'object' && rule.minLength && value && value.length < rule.minLength) {
          errors[field] = `최소 ${rule.minLength}자 이상 입력해주세요.`;
          isValid = false;
          break;
        }
        
        // 최대 길이 검사
        if (typeof rule === 'object' && rule.maxLength && value && value.length > rule.maxLength) {
          errors[field] = `최대 ${rule.maxLength}자까지 입력 가능합니다.`;
          isValid = false;
          break;
        }
        
        // 패턴 검사
        if (typeof rule === 'object' && rule.pattern && value && !new RegExp(rule.pattern).test(value)) {
          errors[field] = rule.message || '형식이 올바르지 않습니다.';
          isValid = false;
          break;
        }
      }
    }
  }
  
  return { isValid, errors };
}