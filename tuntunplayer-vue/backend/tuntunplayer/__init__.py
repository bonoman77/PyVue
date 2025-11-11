import os
from flask import Flask, jsonify
from smpw.utils.file_handler import file_download
from smpw.utils.log_handler import setup_logger
from smpw.config import get_config
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from smpw.swagger import get_swagger_docs

def create_app(config_class=None):
    """애플리케이션 팩토리 함수"""

    app = Flask(__name__)
    # 모든 라우트에 대해 localhost:5173에서 오는 요청 허용
    CORS(app,
        resources={r"/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True,
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],    
    )    
    # 설정 로드
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # 로거 설정
    app = setup_logger(app)

    # 파일 다운로드 URL 규칙 추가
    app.add_url_rule('/file_download', 'file_download', file_download, methods=['GET'])

    
    # Swagger UI 설정
    SWAGGER_URL = '/api/docs'
    API_URL = '/api/swagger.json'
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "SMPW API"
        }
    )
    
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    @app.route('/api/swagger.json')
    def swagger_json():
        return jsonify(get_swagger_docs())


    # 블루프린트 등록
    register_blueprints(app)

    return app

def register_blueprints(app):
    """모든 블루프린트를 앱에 등록"""
    from smpw.router import homes, accounts, todos, boards
    # 각 모듈의 블루프린트 등록
    app.register_blueprint(homes.bp)
    app.register_blueprint(accounts.bp, url_prefix='/accounts')
    app.register_blueprint(todos.bp, url_prefix='/todos')
    app.register_blueprint(boards.bp, url_prefix='/boards')
