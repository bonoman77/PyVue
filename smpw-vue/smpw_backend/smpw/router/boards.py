import smpw.dbconns as conn
from flask import Blueprint, request, jsonify


bp = Blueprint('boards', __name__)


@bp.route("/todo_list", methods=['GET'])
def todo_list():
    user_id = 1
    result = conn.callproc_return_all('sp_get_user_todo_list', [user_id, 1, 10, ''])
    
    # BLOB(bytes) 데이터를 문자열로 디코딩
    for item in result:
        for key, value in item.items():
            if isinstance(value, (bytes, bytearray)):
                item[key] = value.decode('utf-8')
                
    # 응답 데이터 구성
    response_data = {
        'todo_list': result,
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/todo_insert", methods=['POST'])
def todo_insert():
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()
    
    # 필요한 데이터 추출
    title = data.get('title')
    completed = data.get('completed', False)
    
    print(title)
    print(completed)
    
    # 데이터베이스에 저장
    # member_id = session['login_user']['member_id']
    user_id = 1
    result = conn.callproc_return('sp_set_user_todo_insert', [user_id, title, int(completed), ''])
    todo_id = list(result.values())[0] if result else None
    print(todo_id)
    
    # 응답 데이터 구성
    response_data = {
        'todo_id': todo_id,
        'title': title,
        'completed': completed
    }
    
    # JSON 응답 반환
    return jsonify(response_data)
