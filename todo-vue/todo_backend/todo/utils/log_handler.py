import os
import logging
import time
import shutil
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from flask import Flask
import gc  # 가비지 컬렉션 모듈 추가

class SafeRotatingFileHandler(TimedRotatingFileHandler):
    """
    파일 잠금 문제를 방지하는 안전한 로그 로테이션 핸들러
    Windows 환경에서 파일 사용 중 오류를 방지합니다.
    월 말에만 로테이션이 발생하도록 설정되어 있습니다.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rotate_lock = False
        
        # 월 단위 로테이션인 경우 다음 로테이션 시간을 다음 달 1일로 설정
        if self.when == 'M':
            self.computeRollover(int(time.time()))

    def computeRollover(self, currentTime):
        """
        다음 로테이션 시간을 계산합니다.
        월 단위 로테이션인 경우 다음 달 1일로 설정합니다.
        """
        if self.when == 'M':
            # 현재 시간으로부터 다음 달 1일 00:00:00 계산
            current_datetime = datetime.fromtimestamp(currentTime)
            
            # 다음 달 1일 계산
            if current_datetime.month == 12:
                next_month = datetime(current_datetime.year + 1, 1, 1, 0, 0, 0)
            else:
                next_month = datetime(current_datetime.year, current_datetime.month + 1, 1, 0, 0, 0)
                
            self.rolloverAt = int(next_month.timestamp())
            return self.rolloverAt
        else:
            return super().computeRollover(currentTime)

    def emit(self, record):
        """
        로그 레코드 출력 시 파일 잠금 상태를 확인합니다.
        """
        if self.rotate_lock:
            # 로테이션 중이면 잠시 대기
            time.sleep(0.1)
        try:
            super().emit(record)
        except Exception:
            self.handleError(record)

    def doRollover(self):
        """
        로그 파일 회전 시 파일이 사용 중이면 잠시 대기 후 재시도합니다.
        Windows 환경에서는 파일을 직접 복사하는 방식으로 처리합니다.
        """
        self.rotate_lock = True
        try:
            # 로테이션 시작 로그 출력
            print(f"로그 로테이션 시작: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Windows에서는 파일을 먼저 닫아야 함
            if self.stream:
                self.stream.close()
                self.stream = None
                
                # 명시적 가비지 컬렉션 호출
                gc.collect()
                
                # 파일 핸들이 완전히 해제될 시간을 주기 위해 잠시 대기
                time.sleep(0.5)
                print("파일 스트림 닫기 완료 및 가비지 컬렉션 수행")

            # 기존 TimedRotatingFileHandler의 로직 대신 직접 파일 복사 방식 사용
            if os.path.exists(self.baseFilename):
                # 이전 달의 날짜로 백업 파일명 생성
                current_time = time.time()
                current_datetime = datetime.fromtimestamp(current_time)
                
                # 이전 달 계산
                if current_datetime.month == 1:
                    prev_month_datetime = datetime(current_datetime.year - 1, 12, 1)
                else:
                    prev_month_datetime = datetime(current_datetime.year, current_datetime.month - 1, 1)
                
                # 이전 달의 로그 파일명 생성
                dst_filename = self.baseFilename + "." + prev_month_datetime.strftime(self.suffix)
                
                # 이미 존재하는 파일 삭제
                if os.path.exists(dst_filename):
                    try:
                        os.remove(dst_filename)
                    except:
                        pass
                
                # 파일 복사 후 원본 파일 내용 비우기
                try:
                    shutil.copy2(self.baseFilename, dst_filename)
                    # 원본 파일 비우기
                    with open(self.baseFilename, 'w'):
                        pass
                except Exception as e:
                    print(f"로그 로테이션 실패: {str(e)}")
            
            # 다음 로테이션 시간 계산
            self.rolloverAt = self.computeRollover(time.time())
            
            # 파일 다시 열기
            if not self.stream and self.baseFilename:
                self.stream = self._open()
                
        except Exception as e:
            print(f"로그 로테이션 실패: {str(e)}")
        finally:
            self.rotate_lock = False


def setup_logger(app: Flask):
    """
    애플리케이션 로거 설정 함수
    월별로 로그 파일을 분할하여 저장합니다.
    로그 파일은 월 말에 로테이션됩니다.
    로그 파일 이름은 애플리케이션 설정(config)의 APP_NAME에서 가져옵니다.
    """
    # 로그 디렉토리 설정
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 애플리케이션 이름을 config에서 가져옴
    app_name = app.config.get('APP_NAME')
    
    # 로그 파일 설정 - 월별로 로그 분할
    log_file = os.path.join(log_dir, f'{app_name}.log')
    
    file_handler = SafeRotatingFileHandler(
        log_file, 
        when='M',             # 월 단위로 로그 파일 교체 (M: Month)
        interval=1,           # 1개월 간격으로 교체
        backupCount=12,       # 최대 12개의 로그 파일 보관 (약 1년치)
        encoding='utf-8-sig',
        delay=False           # 핸들러 초기화 시 파일 즉시 열기
    )
    # 로그 파일명 형식 설정: APP_NAME.log.YYYY-MM
    file_handler.suffix = "%Y-%m"
    
    # 로그 형식 설정
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    return app