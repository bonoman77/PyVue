import smpw.dbconns as conn
from flask import Blueprint, request, jsonify


bp = Blueprint('boards', __name__)


@bp.route("/board_list", methods=['GET'])
def board_list():
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 10))
    search_text = request.args.get('search_text', '')
    result = conn.callproc_return_all('sp_get_board_list', [page, row_size, search_text])
    total_cnt = conn.callproc_return('sp_get_board_total_cnt', [search_text])
    print(total_cnt)
    # 응답 데이터 구성
    response_data = {
        'board_list': result,
        'total_cnt': total_cnt['cnt'],
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/board_detail/<int:board_id>", methods=['GET'])
def board_detail(board_id):
    result = conn.callproc_return('sp_get_board_select', [board_id])
    # 응답 데이터 구성
    response_data = {
        'board_detail': result,
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/board_delete/<int:board_id>", methods=['DELETE'])
def board_delete(board_id):
    user_id = request.args.get('user_id', type=int)
    conn.callproc_without_return('sp_set_board_delete', [user_id, board_id])
    
    # JSON 응답 반환
    return jsonify({"board_id": board_id})



@bp.route("/board_display/<int:board_id>", methods=['PATCH'])
def board_display(board_id):
    data = request.get_json()
    display_yn = data.get('display_yn')
    conn.callproc_without_return('sp_set_board_display', [board_id, display_yn])
    
    # JSON 응답 반환
    return jsonify({"board_id": board_id})




@bp.route("/board_insert", methods=['POST'])
def board_insert():
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()
    
    # 필요한 데이터 추출
    user_id = data.get('user_id')
    board_kind_id = 1
    title = data.get('title')
    contents = data.get('contents', '')
    print([user_id, board_kind_id, title, contents]) 
    result = conn.callproc_return('sp_set_board_insert', [user_id, board_kind_id, title, contents])
    board_id = list(result.values())[0] if result else None
    
    # 응답 데이터 구성
    response_data = {
        'board_id': board_id,
        'board_kind_id': board_kind_id,
        'title': title,
        'contents': contents
    }
    
    # JSON 응답 반환
    return jsonify(response_data)


@bp.route("/board_update/<int:board_id>", methods=['PUT'])
def board_update(board_id):
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    display_yn = data.get('display_yn')
    contents = data.get('contents', '')
    
    print([user_id, board_id, title, display_yn, contents])

    conn.callproc_without_return('sp_set_board_update', [user_id, board_id, title, int(display_yn), contents])
    
    # JSON 응답 반환
    return jsonify({"board_id": board_id})