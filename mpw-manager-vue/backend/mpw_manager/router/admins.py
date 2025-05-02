import os
import random
import mpw_manager.dbconns as conn
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, url_for, jsonify
from mpw_manager.utils.auth_handler import admin_required
from mpw_manager.utils.page_handler import paged_list
from mpw_manager.utils.mail_handler import send_mail
from mpw_manager.utils.file_handler import FileHandler

bp = Blueprint('admins', __name__)

@bp.route("/index", methods=['GET'])
@admin_required
def index():
    return redirect(url_for('admins.member_list', manager_yn=0))


@bp.route("/member_list/<int:manager_yn>", methods=['GET'])
@admin_required
def member_list(manager_yn):
    search_text = '' if request.args.get('search_text') is None else request.args.get('search_text')
    search = {
        'search_text': search_text,
    }

    proc_cnt = 'uspGetStreamAdminMemberCnt @ManagerYn=?, @SearchText=?'
    total = conn.execute_return(proc_cnt, [manager_yn, search_text]).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)

    proc_list = 'uspGetStreamAdminMemberList @ManagerYn=?, @PageSize=?, @PageNumber=?, @SearchText=?'
    params = [manager_yn, row_size, page, search_text]
    res_list = conn.return_list(proc_list, params)

    return render_template('admins/member_list.html', manager_yn=manager_yn, res_list=res_list
                           , search=search, paging=paging)


@bp.route("/member_login", methods=['GET'])
@admin_required
def member_login():
    member_id = request.args.get('member_id')
    proc = 'uspGetStreamAdminMemberLogIn @MemberID=?'
    res = conn.execute_return(proc, member_id)

    if not res.AuthYn:
        flash("먼저 이메일 인증을 해주셔야 사이트 이용이 가능합니다.", category="rose")
        return render_template('accounts/login.html')

    if res:
        session['login_user'] = {
            'member_id': res.MemberID,
            'member_name': res.MemberName,
            'manager_yn': res.ManagerYn,
            'pass_member_id': res.PassMemberID,
        }

        next_route = session.pop('next', '/')
        return redirect(next_route)
    else:
        flash("해당 사용자가 존재하지 않습니다.", category="rose")
        return render_template('accounts/login.html')


@bp.route("/member_detail/<int:manager_yn>/<int:member_id>", methods=['GET'])
@admin_required
def member_detail(manager_yn, member_id):
    proc_code = 'uspGetStreamMemberCodeList @MemberID=?'
    code_list = conn.return_list(proc_code, member_id)

    proc = 'uspGetStreamMemberDetail @MemberID=?'
    res = conn.execute_return(proc, member_id)

    return render_template('admins/member_detail.html', res=res, manager_yn=manager_yn, code_list=code_list)


@bp.route("/member_delete", methods=['POST'])
@admin_required
def member_delete():
    member_id = request.form.get('member_id')
    admin_member_id = session['login_user']['member_id']

    proc = 'uspSetStreamMemberOut @MemberID=?, @DeleteMemberID=?'
    conn.execute_without_return(proc, [member_id, admin_member_id])

    return jsonify({"result": "success"})


@bp.route('/auth_mail_resend', methods=['POST'])
def auth_mail_resend_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))

    member_id = request.form.get('member_id')
    proc = 'uspSetStreamAdminEmailReAuthRequest @MemberID=?, @AuthCode=?'
    res = conn.execute_return(proc, [member_id, auth_code])
    send_mail(res.UserEmail, res.MemberName, auth_code, 're_auth')
    return jsonify({"result": "success"})


@bp.route('/auth_mail_update', methods=['POST'])
def auth_mail_update_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))

    member_id = request.form.get('member_id')
    user_email = request.form.get('user_email')
    proc = 'uspSetStreamAdminEmailUpdate @MemberID=?, @UserEmail=?, @AuthCode=?'
    res = conn.execute_return(proc, [member_id, user_email, auth_code])
    if res.Result == 9:
        error_message = "동일한 이메일 계정이 존재합니다. 변경할 수 없습니다."
        return jsonify({"result": "", "message": error_message})
    else:
        send_mail(res.UserEmail, res.MemberName, auth_code, 're_auth')
        return jsonify({"result": "success"})


@bp.route('/member_pass_reset', methods=['POST'])
def member_pass_reset_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))

    member_id = request.form.get('member_id')
    proc = 'uspSetStreamAdminPassReset @MemberID=?, @AuthCode=?'
    res = conn.execute_return(proc, [member_id, auth_code])
    send_mail(res.UserEmail, res.MemberName, auth_code, 'reset_passwd')
    return jsonify({"result": "success"})


@bp.route("/version_history")
@admin_required
def version_history():
    return render_template('admins/version_history.html')


@bp.route("/modal_notice_list", methods=['GET'])
@admin_required
def modal_notice_list():
    display_type = int(request.args.get('display_type') or 2)

    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=5)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', '')

    search = {
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
        'display_type': display_type,
    }

    params = [search_text, start_date, end_date, display_type]
    total = conn.execute_return('uspGetStreamAdminModalNoticeTotalCnt \
        @SearchText=?,  @StartDate=?,  @EndDate=?, @DisplayType=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)

    params = [row_size, page, search_text, start_date, end_date, display_type]
    res_list = conn.return_list('uspGetStreamAdminModalNoticeList \
         @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?, @DisplayType=?', params)

    return render_template('admins/modal_notice_list.html', res_list=res_list, search=search,
                           paging=paging)


@bp.route("/modal_notice_insert", methods=['GET'])
@admin_required
def modal_notice_insert():

    return render_template('admins/modal_notice_insert.html')


@bp.route("/modal_notice_insert", methods=['POST'])
@admin_required
def modal_notice_insert_post():
    member_id = session['login_user']['member_id']
    title = request.form.get("title")
    comments = request.form.get("comments")
    link_address = request.form.get("link_address")
    link_address = None if link_address == 'https://' else link_address
    open_date = request.form.get("open_date")
    close_date = request.form.get("close_date") or None

    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], "modal_notice")
    upload_files = request.files.getlist("upload_file_path")

    if len(upload_files) == 0:
        upload_path = None
        file_name_str = None
    else:
        file_handler = FileHandler(upload_path)
        file_name_str = file_handler.file_upload(upload_files)

    params = [member_id, title, comments, link_address, open_date, close_date, upload_path, file_name_str]
    conn.execute_without_return('uspSetStreamAdminModalNoticeInsert @MemberID=?, @Title=?, @Comments=?\
            ,@LinkAddress=?, @OpenDate=?, @CloseDate=?, @UploadFilePath=?, @FileNameString=?', params)

    return redirect(url_for('admins.modal_notice_list'))


@bp.route("/modal_notice_update/<int:modal_notice_id>", methods=['GET'])
@admin_required
def modal_notice_update(modal_notice_id):
    res = conn.execute_return("uspGetStreamAdminModalNoticeDetail @ModalNoticeID=?", modal_notice_id)
    return render_template('admins/modal_notice_update.html', res=res)


@bp.route("/modal_notice_update", methods=['POST'])
@admin_required
def modal_notice_update_post():
    member_id = session['login_user']['member_id']
    modal_notice_id = int(request.form.get("modal_notice_id"))

    title = request.form.get("title")
    comments = request.form.get("comments")
    link_address = request.form.get("link_address")
    link_address = None if link_address == 'https://' else link_address

    open_date = request.form.get("open_date")
    close_date = request.form.get("close_date") or None

    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], 'ModalNotice')
    upload_files = request.files.getlist("upload_file_path")

    if len(upload_files) == 0:
        upload_path = None
        file_name_str = None
    else:
        file_handler = FileHandler(upload_path)
        file_name_str = file_handler.file_upload(upload_files)

    params = [modal_notice_id, member_id, title, comments, link_address, open_date, close_date, upload_path, file_name_str]
    conn.execute_without_return('uspSetStreamAdminModalNoticeUpdate \
            @ModalNoticeID=?, @MemberID=?, @Title=?, @Comments=?, @LinkAddress=?, @OpenDate=?, @CloseDate=?, \
            @UploadFilePath=?, @FileNameString=?', params)

    return redirect(url_for('admins.modal_notice_list'))


@bp.route("/modal_notice_display_update", methods=['POST'])
@admin_required
def modal_notice_display_update():
    modal_notice_id = request.form.get('modal_notice_id')
    display_yn = request.form.get('display_yn')

    proc = 'uspSetStreamAdminModalNoticeDisplayYn @ModalNoticeID=?, @DisplayYn=?'
    conn.execute_without_return(proc, [modal_notice_id, display_yn])

    return jsonify({"result": "success"})


@bp.route("/modal_notice_file_delete", methods=['POST'])
@admin_required
def modal_notice_file_delete():
    modal_notice_id = request.form.get('modal_notice_id')
    proc = 'uspSetStreamAdminModalNoticeFileDelete @ModalNoticeID=?'
    conn.execute_without_return(proc, modal_notice_id)

    return jsonify({"result": "success"})


@bp.route("/modal_notice_delete", methods=['POST'])
@admin_required
def modal_notice_delete():
    modal_notice_id = request.form.get('modal_notice_id')
    proc = '[uspSetStreamAdminModalNoticeDelete] @ModalNoticeID=?'
    conn.execute_without_return(proc, modal_notice_id)

    return jsonify({"result": "success"})
