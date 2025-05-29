import os, atexit
from flask import Flask, url_for
from channel_manager.utils.file_handler import file_download
from channel_manager.utils.log_handler import setup_logger
from channel_manager.config import get_config

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
                # 개발 모드에서만 파일 수정 시간을 쿼리 파라미터로 추가
                if app.debug:
                    file_path = os.path.join(app.root_path, endpoint, filename)
                    if os.path.exists(file_path):
                        values['q'] = int(os.stat(file_path).st_mtime)
                # 프로덕션 모드에서는 버전 번호를 사용하여 캐싱 최적화
                else:
                    # 애플리케이션 버전 또는 배포 시간을 기반으로 한 정적 값 사용
                    values['v'] = app.config.get('STATIC_VERSION', '1.0.0')
        return url_for(endpoint, **values)
    
    # 필터 등록
    with app.app_context():
        import channel_manager.filters
        channel_manager.filters.init_app(app)

    # 블루프린트 등록
    register_blueprints(app)
    
    # 스케줄러 설정
    from channel_manager.router.schedules import start_scheduler, stop_scheduler
    
    # 디버그 모드에서만 스케줄러 초기화 
    try:
        if app.debug:
            if os.environ.get('WERKZEUG_RUN_MAIN'):
                with app.app_context():
                    start_scheduler(app)
    except Exception as e:
        app.logger.error(f"스케줄러 초기화 중 오류 발생: {str(e)}")
    
    atexit.register(lambda: app.app_context().push() and stop_scheduler())
    
    return app

def register_blueprints(app):
    """모든 블루프린트를 앱에 등록"""
    from channel_manager.router import homes, accounts, admins, counsels, sources, manages, emails, schedules
    
    # 각 모듈의 블루프린트 등록
    app.register_blueprint(homes.bp)
    app.register_blueprint(accounts.bp, url_prefix='/accounts')
    app.register_blueprint(admins.bp, url_prefix='/admins')
    app.register_blueprint(counsels.bp, url_prefix='/counsels')
    app.register_blueprint(sources.bp, url_prefix='/sources')
    app.register_blueprint(manages.bp, url_prefix='/manages')
    app.register_blueprint(emails.bp, url_prefix='/emails')
    app.register_blueprint(schedules.bp, url_prefix='/schedules')
