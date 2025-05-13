import smpw.dbconns as conn
from flask import Blueprint, request, jsonify


bp = Blueprint('boards', __name__)


@bp.route("/todo_list", methods=['GET'])
def todo_list():
    user_id = 1
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 10))
    search_text = request.args.get('search_text', '')
    result = conn.callproc_return_all('sp_get_user_todo_list', [user_id, page, row_size, search_text])
    total_cnt = conn.callproc_return('sp_get_user_todo_total_cnt', [user_id, search_text])
    # 응답 데이터 구성
    response_data = {
        'todo_list': result,
        'total_cnt': total_cnt['cnt'],
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/todo_delete/<int:todo_id>", methods=['DELETE'])
def todo_delete(todo_id):
    conn.callproc_without_return('sp_set_user_todo_delete', [todo_id])
    
    # JSON 응답 반환
    return jsonify({"todo_id": todo_id})

@bp.route("/todo_toggle/<int:todo_id>/<int:completed>", methods=['PATCH'])
def todo_toggle(todo_id, completed):
    print(todo_id, completed)
    conn.callproc_without_return('sp_set_user_todo_toggle', [todo_id, completed])
    
    # JSON 응답 반환
    return jsonify({"todo_id": todo_id})

@bp.route("/todo_insert", methods=['POST'])
def todo_insert():
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()
    
    # 필요한 데이터 추출
    title = data.get('title')
    completed = data.get('completed', False)
    
    # 데이터베이스에 저장
    # member_id = session['login_user']['member_id']
    user_id = 1
    result = conn.callproc_return('sp_set_user_todo_insert', [user_id, title, int(completed), ''])
    todo_id = list(result.values())[0] if result else None
    
    # 응답 데이터 구성
    response_data = {
        'todo_id': todo_id,
        'title': title,
        'completed': completed
    }
    
    # JSON 응답 반환
    return jsonify(response_data)
