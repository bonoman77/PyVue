import smpw.dbconns as conn
from flask import Blueprint, request, jsonify


bp = Blueprint('boards', __name__)


@bp.route("/board_list", methods=['GET'])
def board_list():
    user_id = request.args.get('userId', type=int)
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 10))
    search_text = request.args.get('search_text', '')
    result = conn.callproc_return_all('sp_get_board_list', [user_id, page, row_size, search_text])
    total_cnt = conn.callproc_return('sp_get_board_total_cnt', [user_id, search_text])
    # 응답 데이터 구성
    response_data = {
        'board_list': result,
        'total_cnt': total_cnt['cnt'],
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/board_detail/<int:board_id>", methods=['GET'])
def board_detail(board_id):
    user_id = request.args.get('userId', type=int)
    result = conn.callproc_return('sp_get_board_select', [user_id, board_id])
    # 응답 데이터 구성
    response_data = {
        'board_detail': result,
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/board_delete/<int:board_id>", methods=['DELETE'])
def board_delete(board_id):
    user_id = request.args.get('userId', type=int)
    conn.callproc_without_return('sp_set_board_delete', [user_id, board_id])
    
    # JSON 응답 반환
    return jsonify({"board_id": board_id})
    
@bp.route("/board_insert", methods=['POST'])
def board_insert():
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()
    
    # 필요한 데이터 추출
    user_id = data.get('userId')
    title = data.get('title')
    completed = data.get('completed', False)
    contents = data.get('contents', '')
    result = conn.callproc_return('sp_set_board_insert', [user_id, title, int(completed), contents])
    board_id = list(result.values())[0] if result else None
    
    # 응답 데이터 구성
    response_data = {
        'board_id': board_id,
        'title': title,
        'completed': completed,
        'contents': contents
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/board_update/<int:board_id>", methods=['PUT'])
def board_update(board_id):
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()

    user_id = data.get('userId')
    title = data.get('title')
    completed = data.get('completed', False)
    contents = data.get('contents', '')
    
    conn.callproc_without_return('sp_set_board_update', [user_id, board_id, title, int(completed), contents])
    
    # JSON 응답 반환
    return jsonify({"board_id": board_id})