import smpw.dbconns as conn
from flask import Blueprint, render_template

bp = Blueprint('homes', __name__)

@bp.route("/")
def index():
    # 데이터베이스 연결 상태 확인
    db_status = "정상"
    try:
        # 간단한 쿼리로 데이터베이스 연결 테스트
        conn.execute_return('SELECT 1')
    except Exception as e:
        db_status = "연결 실패"
        print(f"데이터베이스 연결 오류: {str(e)}")
    
    # 서버 포트 정보 가져오기
    port = 4000  # start_smpw.py에 설정된 포트
    
    # CORS 허용된 클라이언트 포트 (Vue.js 앱)
    client_port = 5173  # __init__.py의 CORS 설정에서 확인
    
    return render_template('index.html', 
                          db_status=db_status, 
                          server_port=port,
                          client_port=client_port)
