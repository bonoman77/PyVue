import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """기본 설정 클래스"""
    SECRET_KEY = os.environ.get('session_secret_key')
    SESSION_TYPE = 'filesystem'

    # 애플리케이션 이름
    APP_NAME = 'mpw_manager'

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024
    UPLOAD_EXTENSIONS = ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG", "txt", "doc", "docx", "xls", "xlsx", "pdf", "ppt", "pptx", "mp3", "stk"]
    UPLOAD_IMAGES = ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"]
    
    # 메일 설정
    MAIL_SERVER = 'gw.tuntun.co.kr'
    MAIL_PORT = 25
    MAIL_USE_TLS = False 
    MAIL_USERNAME = os.environ.get('email_user')
    MAIL_PASSWORD = os.environ.get('email_password')
    MAIL_DEFAULT_SENDER = ('대도시공개증거관리', 'noreply@tuntun.co.kr')
    MAIL_ASCII_ATTACHMENTS = False
    
    # OpenAI API 키
    OPENAI_API_KEY = os.environ.get('openai_api_key')
    
    # 세션 설정
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = 'mpw_manager_session'


class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    UPLOAD_FOLDER = r"C:\SeungKyun\PyProject\Uploads\MPWManager"  # 로컬 경로


class ProductionConfig(Config):
    """운영 환경 설정"""
    DEBUG = False
    UPLOAD_FOLDER = r"\\172.16.0.244\naspath\MPWManager"  # 서버 경로
    SESSION_COOKIE_SECURE = True  # HTTPS에서만 쿠키 전송


# 환경별 설정 매핑
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """환경 변수에 따라 적절한 설정 반환"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])