// 브라우저 정보 확인
const browser = getBrowser();
console.log(`브라우저: ${browser.name} ${browser.version}`);

// 운영체제 확인
const os = getOS();
console.log(`운영체제: ${os.name} ${os.version}`);

// 디바이스 유형 확인
const deviceType = getDeviceType();
console.log(`디바이스 유형: ${deviceType}`);

// 화면 정보 확인
const screen = getScreenInfo();
console.log(`화면 크기: ${screen.width}x${screen.height}, 방향: ${screen.orientation}`);

// 다크 모드 감지
console.log(`다크 모드: ${isDarkMode() ? '활성화' : '비활성화'}`);

// 다크 모드 변경 감지
const removeListener = watchDarkMode((isDark) => {
  console.log(`다크 모드가 ${isDark ? '활성화' : '비활성화'}되었습니다.`);
  // 테마 변경 로직 실행
});

// 나중에 리스너 제거
// removeListener();

// 모든 정보 한번에 가져오기
const info = getBrowserInfo();
console.log(info);