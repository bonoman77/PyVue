/**
 * 브라우저 및 디바이스 감지 관련 유틸리티 함수
 */

/**
 * 현재 사용자 에이전트 문자열
 * @type {string}
 */
const userAgent = typeof navigator !== 'undefined' ? navigator.userAgent : '';

/**
 * 브라우저 정보 객체
 * @returns {Object} 브라우저 이름과 버전 정보
 */
export function getBrowser() {
  if (typeof window === 'undefined' || !userAgent) {
    return { name: 'unknown', version: 'unknown' };
  }

  // Edge (Chromium 기반)
  if (userAgent.indexOf('Edg') > -1) {
    return {
      name: 'Edge',
      version: userAgent.match(/Edg\/([0-9.]+)/)?.[1] || 'unknown'
    };
  }
  
  // Chrome
  if (userAgent.indexOf('Chrome') > -1 && userAgent.indexOf('Edg') === -1) {
    return {
      name: 'Chrome',
      version: userAgent.match(/Chrome\/([0-9.]+)/)?.[1] || 'unknown'
    };
  }
  
  // Firefox
  if (userAgent.indexOf('Firefox') > -1) {
    return {
      name: 'Firefox',
      version: userAgent.match(/Firefox\/([0-9.]+)/)?.[1] || 'unknown'
    };
  }
  
  // Safari
  if (userAgent.indexOf('Safari') > -1 && userAgent.indexOf('Chrome') === -1) {
    return {
      name: 'Safari',
      version: userAgent.match(/Version\/([0-9.]+)/)?.[1] || 'unknown'
    };
  }
  
  // Opera
  if (userAgent.indexOf('OPR') > -1 || userAgent.indexOf('Opera') > -1) {
    return {
      name: 'Opera',
      version: (userAgent.match(/OPR\/([0-9.]+)/) || userAgent.match(/Opera\/([0-9.]+)/))?.[1] || 'unknown'
    };
  }
  
  // IE
  if (userAgent.indexOf('Trident') > -1) {
    return {
      name: 'Internet Explorer',
      version: userAgent.match(/rv:([0-9.]+)/)?.[1] || 'unknown'
    };
  }
  
  return { name: 'unknown', version: 'unknown' };
}

/**
 * 운영체제 정보 객체
 * @returns {Object} 운영체제 이름과 버전 정보
 */
export function getOS() {
  if (typeof window === 'undefined' || !userAgent) {
    return { name: 'unknown', version: 'unknown' };
  }

  // Windows
  if (userAgent.indexOf('Windows') > -1) {
    const version = userAgent.match(/Windows NT ([0-9.]+)/)?.[1] || 'unknown';
    let name = 'Windows';
    
    // Windows 버전 매핑
    const versionMap = {
      '10.0': '10',
      '6.3': '8.1',
      '6.2': '8',
      '6.1': '7',
      '6.0': 'Vista',
      '5.2': 'XP',
      '5.1': 'XP'
    };
    
    if (versionMap[version]) {
      name += ' ' + versionMap[version];
    }
    
    return { name, version };
  }
  
  // macOS
  if (userAgent.indexOf('Macintosh') > -1 || userAgent.indexOf('Mac OS X') > -1) {
    const version = userAgent.match(/Mac OS X ([0-9._]+)/)?.[1]?.replace(/_/g, '.') || 'unknown';
    return { name: 'macOS', version };
  }
  
  // iOS
  if (userAgent.indexOf('iPhone') > -1 || userAgent.indexOf('iPad') > -1 || userAgent.indexOf('iPod') > -1) {
    const version = userAgent.match(/OS ([0-9_]+)/)?.[1]?.replace(/_/g, '.') || 'unknown';
    return { name: 'iOS', version };
  }
  
  // Android
  if (userAgent.indexOf('Android') > -1) {
    const version = userAgent.match(/Android ([0-9.]+)/)?.[1] || 'unknown';
    return { name: 'Android', version };
  }
  
  // Linux
  if (userAgent.indexOf('Linux') > -1) {
    return { name: 'Linux', version: 'unknown' };
  }
  
  return { name: 'unknown', version: 'unknown' };
}

/**
 * 디바이스 유형 확인
 * @returns {string} 디바이스 유형 (mobile, tablet, desktop)
 */
export function getDeviceType() {
  if (typeof window === 'undefined' || !userAgent) {
    return 'unknown';
  }
  
  // 모바일 기기 확인
  const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i;
  
  // 태블릿 확인
  const tabletRegex = /iPad|Android(?!.*Mobile)/i;
  
  if (tabletRegex.test(userAgent)) {
    return 'tablet';
  } else if (mobileRegex.test(userAgent)) {
    return 'mobile';
  }
  
  return 'desktop';
}

/**
 * 터치 디바이스 여부 확인
 * @returns {boolean} 터치 디바이스이면 true, 아니면 false
 */
export function isTouchDevice() {
  if (typeof window === 'undefined') {
    return false;
  }
  
  return (
    ('ontouchstart' in window) ||
    (navigator.maxTouchPoints > 0) ||
    (navigator.msMaxTouchPoints > 0)
  );
}

/**
 * 화면 크기 정보
 * @returns {Object} 화면 너비, 높이, 방향 정보
 */
export function getScreenInfo() {
  if (typeof window === 'undefined') {
    return { width: 0, height: 0, orientation: 'unknown' };
  }
  
  const width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
  const height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
  const orientation = width > height ? 'landscape' : 'portrait';
  
  return { width, height, orientation };
}

/**
 * 브라우저 기능 지원 여부 확인
 * @returns {Object} 다양한 브라우저 기능 지원 여부
 */
export function getFeatureSupport() {
  if (typeof window === 'undefined') {
    return {
      localStorage: false,
      sessionStorage: false,
      cookies: false,
      webp: false,
      webgl: false,
      canvas: false
    };
  }
  
  // localStorage 지원 여부
  let localStorage = false;
  try {
    localStorage = !!window.localStorage;
  } catch (e) {
    // 일부 브라우저에서 개인정보 보호 모드에서는 접근 시 예외 발생
  }
  
  // sessionStorage 지원 여부
  let sessionStorage = false;
  try {
    sessionStorage = !!window.sessionStorage;
  } catch (e) {
    // 일부 브라우저에서 개인정보 보호 모드에서는 접근 시 예외 발생
  }
  
  // 쿠키 지원 여부
  const cookies = navigator.cookieEnabled;
  
  // Canvas 지원 여부
  const canvas = !!document.createElement('canvas').getContext;
  
  // WebGL 지원 여부
  let webgl = false;
  try {
    const canvas = document.createElement('canvas');
    webgl = !!(window.WebGLRenderingContext && 
      (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
  } catch (e) {
    // WebGL을 지원하지 않는 경우
  }
  
  // WebP 지원 여부는 비동기적으로 확인해야 하므로 여기서는 미정으로 설정
  const webp = false;
  
  return {
    localStorage,
    sessionStorage,
    cookies,
    webp,
    webgl,
    canvas
  };
}

/**
 * WebP 이미지 형식 지원 여부 확인 (비동기)
 * @returns {Promise<boolean>} WebP 지원 여부
 */
export function checkWebpSupport() {
  return new Promise(resolve => {
    const webpImg = new Image();
    webpImg.onload = function() {
      resolve(webpImg.width === 1);
    };
    webpImg.onerror = function() {
      resolve(false);
    };
    webpImg.src = 'data:image/webp;base64,UklGRiQAAABXRUJQVlA4IBgAAAAwAQCdASoBAAEAAwA0JaQAA3AA/vuUAAA=';
  });
}

/**
 * 브라우저 언어 정보 가져오기
 * @returns {string} 브라우저 언어 코드
 */
export function getBrowserLanguage() {
  if (typeof navigator === 'undefined') {
    return 'unknown';
  }
  
  return navigator.language || navigator.userLanguage || 'unknown';
}

/**
 * 다크 모드 감지
 * @returns {boolean} 다크 모드이면 true, 아니면 false
 */
export function isDarkMode() {
  if (typeof window === 'undefined') {
    return false;
  }
  
  return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

/**
 * 다크 모드 변경 감지 이벤트 리스너 설정
 * @param {Function} callback - 다크 모드 변경 시 호출할 콜백 함수
 * @returns {Function} 이벤트 리스너 제거 함수
 */
export function watchDarkMode(callback) {
  if (typeof window === 'undefined' || !window.matchMedia) {
    return () => {};
  }
  
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  
  const listener = (e) => {
    callback(e.matches);
  };
  
  // 이벤트 리스너 추가
  if (mediaQuery.addEventListener) {
    mediaQuery.addEventListener('change', listener);
  } else if (mediaQuery.addListener) {
    // Safari 13.1 이전 버전 지원
    mediaQuery.addListener(listener);
  }
  
  // 이벤트 리스너 제거 함수 반환
  return () => {
    if (mediaQuery.removeEventListener) {
      mediaQuery.removeEventListener('change', listener);
    } else if (mediaQuery.removeListener) {
      mediaQuery.removeListener(listener);
    }
  };
}

/**
 * 브라우저 전체 정보 가져오기
 * @returns {Object} 브라우저, OS, 디바이스, 화면 정보를 포함한 객체
 */
export function getBrowserInfo() {
  return {
    browser: getBrowser(),
    os: getOS(),
    deviceType: getDeviceType(),
    isTouchDevice: isTouchDevice(),
    screen: getScreenInfo(),
    features: getFeatureSupport(),
    language: getBrowserLanguage(),
    isDarkMode: isDarkMode()
  };
}
