import random
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, url_for, jsonify
import mpw_manager.dbconns as conn
from mpw_manager.utils.auth_handler import login_required
from mpw_manager.utils.mail_handler import send_mail

bp = Blueprint('accounts', __name__)

@bp.route("/login", methods=['GET'])
def login():
    if session.get('login_user'):
        return redirect(url_for('homes.index'))

    return render_template('accounts/login.html')


@bp.route('/login', methods=['POST'])
def login_post():
    user_email = request.form.get('user_email')
    user_passwd = request.form.get('user_passwd')

    proc = "uspGetStreamMemberLogInConfirm  @UserEmail=?, @UserPassword=?"
    res = conn.execute_return(proc, [user_email, user_passwd])

    if res:
        if not res.AuthYn:
            flash("먼저 이메일 인증을 해주셔야 사이트 이용이 가능합니다.", category="rose")
            return render_template('accounts/login.html', user_email=user_email)

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
        return render_template('accounts/login.html', user_email=user_email)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        manager_yn = session['login_user']['manager_yn']
    except KeyError:
        manager_yn = 0

    del session['login_user']
    return redirect(url_for('accounts.login', manager_yn=manager_yn))


@bp.route('/accounts/member_insert/<int:manager_yn>', methods=['GET'])
def member_insert(manager_yn):
    if session.get('login_user'):
        return redirect(url_for('homes.index'))

    return render_template('accounts/member_insert.html', manager_yn=manager_yn)


@bp.route('/member_insert', methods=['POST'])
def member_insert_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))
    api_code = "".join(random.choice(alphabet) for _ in range(4))

    service_kind_id = int(request.form.get('service_kind_id'))
    manager_yn = int(request.form.get('manager_yn'))
    member_code = request.form.get('member_code')
    member_name = request.form.get('member_name')
    user_email = request.form.get('user_email')
    user_passwd = request.form.get('user_passwd')

    proc = 'uspSetStreamMemberInsert @ServiceKindID=?, @ManagerYn=?, @MemberCode=?, @MemberName=? \
                        , @UserEmail=?, @UserPassword=?, @AuthCode=? ,@ApiCode=?'
    params = [service_kind_id, manager_yn, member_code, member_name, user_email, user_passwd, auth_code, api_code]

    res = int(conn.execute_return(proc, params)[0])

    if res == 1:
        send_mail(user_email, member_name, auth_code, 'register')
        return redirect(url_for('accounts.welcome', user_email=user_email))
    else:
        error_messages = {
            0: "등록된 회원/교사가 아닙니다.",
            2: "이미 사용중인 이메일입니다.",
            3: "이미 사용중인 회원코드입니다.",
            4: "회원코드 혹은 회원/교사명이 잘못되었습니다."
        }
        flash(error_messages.get(res, "알 수 없는 오류가 발생했습니다."), category="warning")

    return render_template('accounts/member_insert.html')


@bp.route('/welcome', methods=['GET'])
def welcome():
    user_email = request.args.get('user_email')

    model_num = random.choice(range(1, 10))
    model_path = f"/static/images/notice/illust_{model_num}.png"
    return render_template('accounts/welcome.html', user_email=user_email, model_path=model_path)


@bp.route('/member_update', methods=['GET'])
@login_required
def member_update():
    member_id = session['login_user']['member_id']

    proc_code = "uspGetStreamMemberCodeList @MemberID=?"
    code_list = conn.return_list(proc_code, member_id)

    proc = "uspGetStreamMemberDetail @MemberID=?"
    res = conn.execute_return(proc, member_id)

    return render_template('accounts/member_update.html', res=res, code_list=code_list)


@bp.route('/member_pass_update', methods=['GET'])
@login_required
def member_pass_update():
    return render_template('accounts/member_pass_update.html')


@bp.route('/member_pass_update', methods=['POST'])
@login_required
def member_pass_update_post():
    member_id = session['login_user']['member_id']
    old_passwd = request.form.get('old_passwd')
    new_passwd = request.form.get('new_passwd')
    confirm_passwd = request.form.get('confirm_passwd')

    if new_passwd != confirm_passwd:
        flash("입력한 암호가 서로 일치하지 않습니다.", category="rose")
        return render_template('accounts/member_pass_update.html')

    proc = 'uspGetStreamMemberPassConfirm @MemberID=?, @UserPassword=?'
    member_yn = int(conn.execute_return(proc, [member_id, old_passwd]).MemberYn)

    if not member_yn:
        flash("기존 암호가 잘못되었습니다.", category="rose")
        return render_template('accounts/member_pass_update.html')

    proc = 'uspSetStreamMemberUserPassUpdate @MemberID=?, @UserPassword=?'
    conn.execute_without_return(proc, [member_id, new_passwd])

    flash("암호가 정상적으로 수정되었습니다.", category="info")
    return redirect(url_for('homes.index'))


@bp.route("/member_code_search", methods=['POST'])
def member_code_search():
    if session.get('login_user'):
        control_member_id = session['login_user']['member_id']
        proc_admin = 'uspGetStreamMemberAdminYn @MemberID=?'
        admin_yn = bool(conn.execute_return(proc_admin, control_member_id).AdminYn)
    else:
        admin_yn = False

    add_yn = request.form.get('add_yn', 0)
    member_id = request.form.get('member_id', 0)

    manager_yn = bool(int(request.form.get('manager_yn')))
    service_kind_id = request.form.get('service_kind_id')
    member_code = request.form.get('member_code')
    member_name = request.form.get('member_name')

    if add_yn:
        if manager_yn:
            proc = 'uspGetStreamSearchTeacherCodeAdd @ServiceKindID=?, @MemberID=?, @MemberCode=?, @MemberName=?, @AdminYn=?'
        else:
            proc = 'uspGetStreamSearchMemberCodeAdd @ServiceKindID=?, @MemberID=?, @MemberCode=?, @MemberName=?, @AdminYn=?'

        params = [service_kind_id, member_id, member_code, member_name, admin_yn]
        res = conn.execute_return(proc, params)
    else:
        if manager_yn:
            proc = 'uspGetStreamSearchTeacherCode @ServiceKindID=?, @MemberCode=?, @MemberName=?'
        else:
            proc = 'uspGetStreamSearchMemberCode @ServiceKindID=?, @MemberCode=?, @MemberName=?'

        params = [service_kind_id, member_code, member_name]
        res = conn.execute_return(proc, params)

    if not res:
        error_message = "등록되지 않은 계정입니다."
        response_data = {"result": "fail", "message": error_message}
    elif res.ErrorNum == 1:
        error_message = "이미 등록되어있는 회원입니다."
        response_data = {"result": "fail", "message": error_message}
    else:
        response_data = {"result": "success"}

    return jsonify(response_data)


@bp.route("/member_account_search", methods=['POST'])
def member_account_search():
    add_yn = request.form.get('add_yn', 0) 
    service_kind_id = request.form.get('service_kind_id')
    account = request.form.get('account')
    passwd = request.form.get('passwd')

    if add_yn:
        member_id = session['login_user']['member_id']
        proc = 'uspGetStreamSearchMemberAccountAdd @ServiceKindID=?, @MemberID=?, @Account=?, @Password=?'
        params = [service_kind_id, member_id, account, passwd]
        res = conn.execute_return(proc, params)
    else:
        proc = 'uspGetStreamSearchMemberAccount @ServiceKindID=?, @Account=?, @Password=?'
        params = [service_kind_id, account, passwd]
        res = conn.execute_return(proc, params)


    if not res:
        error_message = "등록되지 않았거나 제품 미인증 계정입니다."
        response_data = {"result": "fail", "message": error_message}
    elif res.ErrorNum == 1:
        error_message = "이미 등록되어있는 회원입니다."
        response_data = {"result": "fail", "message": error_message}
    else:
        response_data = {"result": "success", "member_code": res.MemberCode, "member_name": res.MemberName}

    return jsonify(response_data)


@bp.route('/auth_mail_resend', methods=['GET'])
def auth_mail_resend():
    if session.get('login_user'):
        return redirect(url_for('homes.index'))

    return render_template('accounts/auth_mail_resend.html')


@bp.route('/auth_mail_resend', methods=['POST'])
def auth_mail_resend_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))

    user_email = request.form.get('user_email')
    user_passwd = request.form.get('user_passwd')
    member_name = request.form.get('member_name')

    proc = 'uspSetStreamMemberEmailReAuthRequest @UserEmail=?, @UserPassword=?, @MemberName=?, @AuthCode=?'
    params = [user_email, user_passwd, member_name, auth_code]
    res = conn.execute_return(proc, params)[0]

    if not res:
        flash("등록된 계정이 아닙니다. 다시 확인해 해주세요.", category="rose")
        return render_template('accounts/auth_mail_resend.html', user_email=user_email, member_name=member_name)

    send_mail(user_email, member_name, auth_code, 're_auth')
    flash("인증 메일이 재발송 완료되었습니다. 개인 메일을 확인해주세요.", category="success")
    return redirect(url_for('homes.index'))


@bp.route('/member_pass_reset', methods=['GET'])
def member_pass_reset():
    if session.get('login_user'):
        return redirect(url_for('homes.index'))

    return render_template('accounts/member_pass_reset.html')


@bp.route('/member_pass_reset', methods=['POST'])
def member_pass_reset_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))

    user_email = request.form.get('user_email')
    member_name = request.form.get('member_name')

    proc = 'uspSetStreamMemberPassReset @UserEmail=?, @MemberName=?, @AuthCode=?'
    params = [user_email, member_name, auth_code]
    res = conn.execute_return(proc, params)[0]

    if not res:
        flash("등록된 계정이 아닙니다. 다시 확인해 해주세요.", category="rose")
        return render_template('accounts/member_pass_reset.html', user_email=user_email, member_name=member_name)

    send_mail(user_email, member_name, auth_code, 'reset_passwd')
    flash("비밀번호 초기화 신청이 완료되었습니다. 개인 메일을 확인해 해주세요.", category="success")
    return redirect(url_for('homes.index'))


# 발송된 메일에서 확인하는 경로
@bp.route('/auth', methods=['GET'])
def auth():
    user_email = request.args.get('user_email')
    auth_code = request.args.get('auth_code')

    proc = 'uspSetStreamMemberEmailAuth @UserEmail=?, @AuthCode=?'
    res = int(conn.execute_return(proc, [user_email, auth_code])[0])

    if res == 1:
        flash("이메일 인증이 완료되었습니다. 로그인 해주세요.", category="success")
        return redirect(url_for('accounts.login'))
    else:
        return redirect(url_for('homes.message', msg_kind="auth_fail"))


# 발송된 메일에서 확인하는 경로
@bp.route('/auth_pass_update', methods=['GET'])
def auth_pass_update():
    user_email = request.args.get('user_email')
    auth_code = request.args.get('auth_code')

    proc = 'uspSetStreamMemberPassAuth @UserEmail=?, @AuthCode=?'
    res = int(conn.execute_return(proc, [user_email, auth_code])[0])

    if res == 1:
        flash("이메일 인증이 완료되었습니다. 비밀번호를 변경해 주세요.", category="success")
        return render_template('accounts/auth_pass_update.html', user_email=user_email)
    else:
        return redirect(url_for('homes.message', msg_kind="auth_fail"))


@bp.route('/auth_pass_update', methods=['POST'])
def auth_pass_update_post():
    user_email = request.form.get('user_email')
    new_passwd = request.form.get('new_passwd')
    confirm_passwd = request.form.get('confirm_passwd')

    if new_passwd != confirm_passwd:
        flash("입력한 암호가 서로 일치하지 않습니다.", category="rose")
        return render_template('accounts/auth_pass_update.html', user_email=user_email)

    proc = 'uspSetStreamMemberPassUpdate @UserEmail=?, @UserPassword=?'
    res = int(conn.execute_return(proc, [user_email, new_passwd])[0])

    if not res:
        flash("이메일 계정이 올바르지 않습니다. 변경 요청 절차를 다시 진행해주세요.", category="rose")
        return render_template('accounts/auth_pass_update.html', user_email=user_email)

    flash("암호가 정상적으로 수정되었습니다.", category="info")
    return redirect(url_for('homes.index'))
