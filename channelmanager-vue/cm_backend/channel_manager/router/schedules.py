from flask import Blueprint, current_app, jsonify
from channel_manager.router.emails import send_automated_email
from apscheduler.schedulers.background import BackgroundScheduler
from channel_manager.utils.auth_handler import login_required
from functools import partial, wraps

bp = Blueprint('schedules', __name__)

# 전역 스케줄러 - 강제로 단일 인스턴스 유지
_instance = None
_app = None

def get_scheduler():
    global _instance
    if _instance is None:
        _instance = BackgroundScheduler(
            timezone='Asia/Seoul',
            job_defaults={
                'coalesce': True,
                'max_instances': 1,
                'misfire_grace_time': None
            }
        )
    return _instance


def with_app_context(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global _app
        if _app is not None:
            with _app.app_context():
                return f(*args, **kwargs)
        else:
            # 애플리케이션 컨텍스트가 없을 경우 오류 로깅
            print("오류: 애플리케이션 컨텍스트가 설정되지 않았습니다.")
            return None
    return wrapper


def init_email_scheduler(app=None):
    """이메일 작업 초기화"""
    global _app
    if app is not None:
        _app = app
    
    scheduler = get_scheduler()
    scheduler.remove_all_jobs()
     
    morning_job = partial(send_automated_email, time_group='morning')
    daily_job = partial(send_automated_email, time_group='daily')
    tuntun_order_job = partial(send_automated_email, time_group='tuntun_order_after')
    masterclub_order_job = partial(send_automated_email, time_group='masterclub_order_after')
    
    scheduler.add_job(
        func=with_app_context(morning_job),
        trigger='cron',
        hour=5,
        minute=0,
        id='morning_report',
        name='업무 리포트',
        replace_existing=True, 
        max_instances=1,  
        coalesce=True   
    )

    scheduler.add_job(
        func=with_app_context(daily_job),
        trigger='cron',
        hour=5,
        minute=10,
        id='daily_report',
        name='일간 리포트',
        replace_existing=True, 
        max_instances=1,  
        coalesce=True   
    )

    scheduler.add_job(
        func=with_app_context(masterclub_order_job),
        trigger='cron',
        hour=10,
        minute=10,
        id='masterclub_order_report',
        name='마스터클럽 주문 리포트',
        replace_existing=True,
        max_instances=1,  
        coalesce=True  
    )

    scheduler.add_job(
        func=with_app_context(tuntun_order_job),
        trigger='cron',
        hour=13,
        minute=0,
        id='tuntun_order_report',
        name='사업본부 주문 리포트',
        replace_existing=True,
        max_instances=1,  
        coalesce=True  
    )

    if _app:
        _app.logger.info("스케줄러 초기화 완료")
    else:
        print("스케줄러 초기화 완료")

def start_scheduler(app=None):
    """스케줄러 시작"""
    global _app
    if app is not None:
        _app = app
        
    scheduler = get_scheduler()
    
    try:
        if not scheduler.running:
            init_email_scheduler()
            scheduler.start()
            if _app:
                _app.logger.info("스케줄러가 성공적으로 시작되었습니다")
            else:
                print("스케줄러가 성공적으로 시작되었습니다")
        else:
            scheduler.remove_all_jobs()
            init_email_scheduler()
            if _app:
                _app.logger.info("스케줄러 작업이 성공적으로 업데이트되었습니다")
            else:
                print("스케줄러 작업이 성공적으로 업데이트되었습니다")

        return True
    except Exception as e:
        error_msg = f"스케줄러 시작/업데이트 실패: {str(e)}"
        if _app:
            _app.logger.error(error_msg)
        else:
            print(error_msg)
        return False


def stop_scheduler():
    """서버 종료 시 스케줄러를 안전하게 종료"""
    scheduler = get_scheduler()

    if scheduler and scheduler.running:
        scheduler.shutdown()
        current_app.logger.info("스케줄러가 안전하게 종료되었습니다")


@bp.route("/status")
@login_required
def check_scheduler_status():
    """스케줄러 상태 확인"""
    scheduler = get_scheduler()
    jobs = scheduler.get_jobs()
    
    return jsonify({
        'running': scheduler.running,
        'jobs': [{
            'id': job.id,
            'name': job.name,
            'next_run_time': str(job.next_run_time)
        } for job in jobs]
    })

