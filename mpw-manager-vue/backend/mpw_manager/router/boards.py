import os
import mpw_manager.dbconns as conn
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, url_for, jsonify
from dateutil.relativedelta import relativedelta
from datetime import date, datetime, timedelta

from mpw_manager.enums import ProductKind, BoardKind
from mpw_manager.utils.file_handler import FileHandler
from mpw_manager.utils.auth_handler import login_required, admin_required
from mpw_manager.utils.page_handler import paged_list

bp = Blueprint('boards', __name__)


@bp.route("/todo_insert", methods=['POST'])
def todo_insert():
    # 요청에서 JSON 데이터 가져오기
    data = request.get_json()
    
    # 필요한 데이터 추출
    subject = data.get('subjects')
    completed = data.get('completed', False)
    
    # 여기서 데이터베이스에 저장하는 로직을 구현할 수 있습니다
    # 예: conn.execute_without_return("INSERT INTO todos (subject, completed) VALUES (?, ?)", [subject, completed])
    
    # 저장 후 생성된 todo 항목을 반환
    # 실제로는 데이터베이스에서 생성된 ID를 사용해야 합니다
    todo_id = datetime.now().timestamp()  # 임시 ID 생성
    
    # 응답 데이터 구성
    response_data = {
        'id': todo_id,
        'subject': subject,
        'completed': completed
    }
    
    # JSON 응답 반환
    return jsonify(response_data)



@bp.route("/board_list/<int:board_kind_id>/<int:product_kind_id>", methods=['GET'])
@login_required
def board_list(board_kind_id, product_kind_id):
    member_id = session['login_user']['member_id']

    if board_kind_id == BoardKind.REFERENCE.value and product_kind_id != ProductKind.SPECIAL_CLASS.value:
        proc_auth = 'uspGetStreamManagerServiceKindAuth @MemberID=?, @ProductKindID=?'
        auth_yn = bool(conn.execute_return(proc_auth, [member_id, product_kind_id]).AuthYn)
    else:
        auth_yn = True

    common_board_list = [
        BoardKind.NOTICE.value,
        BoardKind.SPECIAL.value,
        BoardKind.MOMS_CLASS.value,
        BoardKind.CLASS_NEW.value,
        BoardKind.CLASS_SPECIAL.value,
        BoardKind.EDU_CONSULT.value,
    ]

    if board_kind_id in common_board_list:
        product_kind_id = ProductKind.COMMON.value

    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=3)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', '')

    search = {
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }

    proc_cnt = 'uspGetStreamBoardTotalCnt @ProductKindID=?, @BoardKindID=?, @SearchText=?,  @StartDate=?,  @EndDate=?'
    params = [product_kind_id, board_kind_id, search_text, start_date, end_date]
    total = conn.execute_return(proc_cnt, params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    proc_list = 'uspGetStreamBoardList \
        @ProductKindID=?, @BoardKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?,  @StartDate=?,  @EndDate=?'
    paging = paged_list(total, page, paging_line, row_size)

    params = [product_kind_id, board_kind_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list(proc_list, params)

    return render_template('boards/board_list.html', res_list=res_list, search=search,
                           paging=paging, product_kind_id=product_kind_id, board_kind_id=board_kind_id, auth_yn=auth_yn,
                           ProductKind=ProductKind, BoardKind=BoardKind)


@bp.route("/board_detail/<int:board_id>/<int:board_kind_id>/<int:product_kind_id>", methods=['GET'])
@login_required
def board_detail(board_id, board_kind_id, product_kind_id):

    proc_file = 'uspGetStreamBoardFileList @BoardID=?'
    file_list = conn.return_list(proc_file, board_id)

    proc = 'uspGetStreamBoardDetail @BoardID=?'
    res = conn.execute_return(proc, board_id)

    return render_template('boards/board_detail.html', res=res, file_list=file_list
                           , board_kind_id=board_kind_id, product_kind_id=product_kind_id)


@bp.route("/admin_board_list/<int:board_kind_id>/<int:product_kind_id>", methods=['GET'])
@admin_required
def admin_board_list(board_kind_id, product_kind_id):
    specific_board_list = [
        BoardKind.REFERENCE.value,
        BoardKind.EXPERIENCE.value,
        BoardKind.CONSULT.value,
    ]

    if not product_kind_id:
        product_kind_id = ProductKind.BABY_LEAGUE.value if board_kind_id in specific_board_list else ProductKind.COMMON.value
    else:
        product_kind_id = int(product_kind_id)

    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=3)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', '')

    search = {
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }

    proc_cnt = 'uspGetStreamBoardManagerTotalCnt @ProductKindID=?, @BoardKindID=?, @SearchText=?,  @StartDate=?,  @EndDate=?'
    params = [product_kind_id, board_kind_id, search_text, start_date, end_date]
    total = conn.execute_return(proc_cnt, params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)

    proc_list = 'uspGetStreamBoardManagerList \
        @ProductKindID=?, @BoardKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?,  @StartDate=?,  @EndDate=?'
    params = [product_kind_id, board_kind_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list(proc_list, params)

    return render_template('boards/admin_board_list.html', res_list=res_list, search=search,
                           paging=paging, product_kind_id=product_kind_id, board_kind_id=board_kind_id)


@bp.route("/admin_board_insert/<int:board_kind_id>/<int:product_kind_id>", methods=['GET'])
@admin_required
def admin_board_insert(board_kind_id, product_kind_id):

    return render_template('boards/admin_board_insert.html'
                           , board_kind_id=board_kind_id, product_kind_id=product_kind_id)


@bp.route("/admin_board_insert", methods=['POST'])
@admin_required
def admin_board_insert_post():
    member_id = session['login_user']['member_id']
    title = request.form.get('title')
    comments = request.form.get('comments')

    product_kind_id = int(request.form.get('product_kind_id'))
    board_kind_id = int(request.form.get('board_kind_id'))
    subfolder_mapping = {
        104: "Notice",
        105: "Reference",
        106: "Experience",
        107: "Consult",
        110: "MomsClass",
        111: "ClassNew",
        112: "ClassSpecial",
        114: "EduConsult"
    }
    subfolder = subfolder_mapping.get(board_kind_id, "None")

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Board', subfolder)
    upload_files = request.files.getlist('upload_file_path')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamBoardInsert \
            @MemberID=?, @BoardKindID=?, @ProductKindID=?, @Title=?, @Comments=?, @UploadFilePath=?, @FileNameString=?'
    params = [member_id, board_kind_id, product_kind_id, title, comments, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return redirect(url_for('boards.admin_board_list', board_kind_id=board_kind_id, product_kind_id=product_kind_id))


@bp.route("/admin_board_update/<int:board_kind_id>/<int:board_id>", methods=['GET'])
@admin_required
def admin_board_update(board_kind_id, board_id):

    proc_file = 'uspGetStreamBoardFileList @BoardID=?'
    file_list = conn.return_list(proc_file, board_id)

    proc = 'uspGetStreamBoardDetail @BoardID=?'
    res = conn.execute_return(proc, board_id)

    return render_template('boards/admin_board_update.html', res=res, file_list=file_list, board_kind_id=board_kind_id)


@bp.route("/admin_board_update", methods=['POST'])
@admin_required
def admin_board_update_post():
    title = request.form.get('title')
    comments = request.form.get('comments')
    member_id = session['login_user']['member_id']

    board_id = int(request.form.get('board_id'))
    product_kind_id = int(request.form.get('product_kind_id'))
    board_kind_id = int(request.form.get('board_kind_id'))
    subfolder_mapping = {
        104: "Notice",
        105: "Reference",
        106: "Experience",
        107: "Consult",
        110: "MomsClass",
        111: "ClassNew",
        112: "ClassSpecial",
        114: "EduConsult"
    }
    subfolder = subfolder_mapping.get(board_kind_id, "None")

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Board', subfolder)
    upload_files = request.files.getlist('upload_file_path')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamBoardUpdate \
                @MemberID=?, @BoardID=?, @Title=?, @Comments=?, @UploadFilePath=?, @FileNameString=?'
    params = [member_id, board_id, title, comments, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return redirect(url_for('boards.admin_board_list', board_kind_id=board_kind_id, product_kind_id=product_kind_id))


@bp.route("/admin_board_display_update", methods=['POST'])
@admin_required
def admin_board_display_update():
    board_id = request.form.get('board_id')
    display_yn = request.form.get('display_yn')

    proc = 'uspSetStreamBoardDisplayYn @BoardID=?, @DisplayYn=?'
    conn.execute_without_return(proc, [board_id, display_yn])

    return jsonify({"result": "success"})


@bp.route("/admin_board_recommend_update", methods=['POST'])
@admin_required
def admin_board_recommend_update():
    board_id = request.form.get('board_id')
    recommend_yn = request.form.get('recommend_yn')

    proc = 'uspSetStreamBoardRecommendYn @BoardID=?, @RecommendYn=?'
    conn.execute_without_return(proc, [board_id, recommend_yn])

    return jsonify({"result": "success"})


@bp.route("/admin_board_delete", methods=['POST'])
@admin_required
def admin_board_delete():
    board_id = request.form.get('board_id')
    proc = 'uspSetStreamBoardDelete @BoardID=?'
    conn.execute_without_return(proc, board_id)

    return jsonify({"result": "success"})


@bp.route("/admin_board_file_delete", methods=['POST'])
@admin_required
def admin_board_file_delete():
    member_id = session['login_user']['member_id']
    board_file_id = request.form.get('board_file_id')

    proc = 'uspSetStreamBoardFileDelete @MemberID=?, @BoardFileID=?'
    params = [member_id, board_file_id]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})