import os
from flask import Flask, url_for
from tuntun_player.utils.file_handler import file_download
from tuntun_player.utils.log_handler import setup_logger
from tuntun_player.config import get_config

def create_app(config_class=None):
    """애플리케이션 팩토리 함수"""
    app = Flask(__name__)
    
    # 설정 로드
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # 로거 설정
    app = setup_logger(app)

    # 파일 다운로드 URL 규칙 추가
    app.add_url_rule('/file_download', 'file_download', file_download, methods=['GET'])
    
    # 항상 페이지 갱신을 위한 작업 
    @app.context_processor
    def override_url_for():
        return dict(url_for=dated_url_for)
    
    def dated_url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', None)
            if filename:
                file_path = os.path.join(app.root_path, endpoint, filename)
                values['q'] = int(os.stat(file_path).st_mtime)
        return url_for(endpoint, **values)
    
    # 필터 등록
    with app.app_context():
        import tuntun_player.filters
        tuntun_player.filters.init_app(app)

    # 블루프린트 등록
    register_blueprints(app)

    return app

def register_blueprints(app):
    """모든 블루프린트를 앱에 등록"""
    from tuntun_player.router import homes, accounts, admins, boards, products, educations, playgrounds
    # 각 모듈의 블루프린트 등록
    app.register_blueprint(homes.bp)
    app.register_blueprint(accounts.bp, url_prefix='/accounts')
    app.register_blueprint(admins.bp, url_prefix='/admins')
    app.register_blueprint(boards.bp, url_prefix='/boards')
    app.register_blueprint(products.bp, url_prefix='/products')
    app.register_blueprint(educations.bp, url_prefix='/educations')
    app.register_blueprint(playgrounds.bp, url_prefix='/playgrounds')




