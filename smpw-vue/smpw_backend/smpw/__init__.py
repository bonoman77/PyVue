import os
from flask import Flask, url_for
from smpw.utils.file_handler import file_download
from smpw.utils.log_handler import setup_logger
from smpw.config import get_config
from flask_cors import CORS

def create_app(config_class=None):
    """애플리케이션 팩토리 함수"""

    app = Flask(__name__)
    # 모든 라우트에 대해 localhost:5173에서 오는 요청 허용
    CORS(app,
        resources={r"/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],    
    )    
    # 설정 로드
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # 로거 설정
    app = setup_logger(app)

    # 파일 다운로드 URL 규칙 추가
    app.add_url_rule('/file_download', 'file_download', file_download, methods=['GET'])

    
    # 블루프린트 등록
    register_blueprints(app)

    return app

def register_blueprints(app):
    """모든 블루프린트를 앱에 등록"""
    from smpw.router import homes, accounts, admins, boards, manages
    # 각 모듈의 블루프린트 등록
    app.register_blueprint(homes.bp)
    app.register_blueprint(accounts.bp, url_prefix='/accounts')
    app.register_blueprint(admins.bp, url_prefix='/admins')
    app.register_blueprint(boards.bp, url_prefix='/boards')
    app.register_blueprint(manages.bp, url_prefix='/manages')
