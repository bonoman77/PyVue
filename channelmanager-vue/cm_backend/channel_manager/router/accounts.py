from flask import Blueprint, request, session, render_template, url_for, redirect, flash, jsonify
import channel_manager.dbconns as conn
from channel_manager.utils.auth_handler import login_required
from channel_manager.utils.mail_handler import send_mail
from datetime import date, datetime, timedelta
import random

bp = Blueprint('accounts', __name__)

@bp.route('/login', methods=['GET'])
def login():
    if session.get('login_user'):
        return redirect(url_for('homes.index', channel_id=session['login_user']['channel_id']))

    return render_template('accounts/login.html')


@bp.route('/login', methods=['POST'])
def login_post():

    user_email = request.form.get('user_email')
    user_passwd = request.form.get('user_passwd')

    proc = "uspGetChannelUserLogIn @UserEmail=?,  @UserPassword=?"
    params = [user_email, user_passwd]
    res = conn.execute_return(proc, params)

    if res:
        if bool(res.AuthYn):

            session['login_user'] = {
                'user_id': int(res.ChannelUserID),
                'user_name': res.UserName,
                'user_email': res.UserEmail,
                'channel_id': int(res.ChannelKindID),
                'finance_yn': bool(res.FinanceYn),
                'admin_yn': bool(res.AdminYn),
                'head_office_yn': bool(res.HeadOfficeYn), 
            }

            if session.get('next'):
                # 로그인 전 마지막 경로로 이동
                next = session.get('next')
                del session['next']
                return redirect(next)
            return redirect(url_for('homes.index', channel_id=session['login_user']['channel_id']))
        else:
            flash("먼저 이메일 인증을 해주세요.", category="danger")
            return render_template('accounts/login.html', user_email=user_email)
    else:
        flash("입력한 계정이 존재하지 않습니다.", category="danger")
        return render_template('accounts/login.html', user_email=user_email)


@bp.route('/admin_user_login', methods=['POST'])
def admin_user_login_post():

    user_id = request.form.get('user_id')
    res = conn.execute_return("uspGetChannelAdminUserLogIn @ChannelUserID=?", user_id)

    if res:
        if bool(res.AuthYn):

            session['login_user'] = {
                'user_id': int(res.ChannelUserID),
                'user_name': res.UserName,
                'user_email': res.UserEmail,
                'channel_id': int(res.ChannelKindID),
                'finance_yn': bool(res.FinanceYn),
                'admin_yn': bool(res.AdminYn),
                'head_office_yn': bool(res.HeadOfficeYn), 
            }

            if session.get('next'):
                # 로그인 전 마지막 경로로 이동
                next = session.get('next')
                del session['next']
                return redirect(next)
            return redirect(url_for('homes.index', channel_id=session['login_user']['channel_id']))
        else:
            flash("먼저 이메일 인증을 해주세요.", category="danger")
            return render_template('accounts/login.html', user_email=user_email)
    else:
        flash("입력한 계정이 존재하지 않습니다.", category="danger")
        return render_template('accounts/login.html', user_email=user_email)


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    del session['login_user']
    return redirect(url_for('accounts.login'))


@bp.route('/user_term', methods=['GET'])
def user_term():
    return render_template('accounts/user_term.html')


@bp.route('/user_insert', methods=['GET'])
def user_insert():
    return render_template('accounts/user_insert.html')


@bp.route('/user_insert', methods=['POST'])
def user_insert_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))

    user_email = request.form.get('user_email')
    user_name = request.form.get('user_name')
    employee_code = request.form.get('employee_code')
    user_passwd = request.form.get('user_passwd')

    proc = 'uspSetChannelUserRegist @UserEmail=?, @UserName=?, @EmployeeCode=?, @UserPassword=?, @AuthCode=?'
    params = [user_email, user_name, employee_code, user_passwd, auth_code]

    res = int(conn.execute_return(proc, params)[0])

    if res == 1:
        send_mail(user_email, user_name, auth_code, 'register')
        return redirect(url_for('accounts.welcome', user_email=user_email))
    else:
        error_messages = {
            0: "등록에 실패하였습니다. 관리자에게 문의해주세요.",
            2: "이미 사용중인 이메일입니다. 관리자에게 문의해주세요.",
            3: "이미 사용중인 사원코드입니다. 관리자에게 문의해주세요.",
        }
        flash(error_messages.get(res, "알 수 없는 오류가 발생했습니다."), category="warning")   
        return render_template('accounts/user_insert.html')


@bp.route("/welcome", methods=['GET'])
def welcome():
    return render_template('accounts/welcome.html')


@bp.route("/user_update/<int:channel_id>", methods=['GET'])
@login_required
def user_update(channel_id):
    user_id = session['login_user']['user_id']
    res_list = conn.return_list('uspGetChannelUserChannelKindList @ChannelUserID=?', user_id)
    return render_template('accounts/user_update.html', channel_id=channel_id, res_list=res_list)


@bp.route('/user_channel_update', methods=['POST'])
@login_required
def user_channel_update_post():
    user_id = session['login_user']['user_id']
    channel_id = request.form.get('ChannelKindID')

    proc = 'uspSetChannelUserChannelKindUpdate @ChannelUserID=?, @ChannelKindID=?'
    conn.execute_without_return(proc, [user_id, channel_id])

    flash("주요 채널이 정상적으로 수정되었습니다.", category="info")
    return redirect(url_for('homes.index', channel_id=channel_id))


@bp.route('/user_pass_update', methods=['POST'])
@login_required
def user_pass_update_post():
    user_id = session['login_user']['user_id']
    old_passwd = request.form.get('old_passwd')
    new_passwd = request.form.get('new_passwd')
    confirm_passwd = request.form.get('confirm_passwd')

    if new_passwd != confirm_passwd:
        flash("입력한 암호가 서로 일치하지 않습니다.", category="danger")
        return render_template('accounts/user_pass_update.html')

    proc = 'uspGetChannelUserPassConfirm @ChannelUserID=?, @UserPassword=?'
    user_yn = int(conn.execute_return(proc, [user_id, old_passwd]).UserYn)

    if not user_yn:
        flash("기존 암호가 잘못되었습니다.", category="danger")
        return render_template('accounts/user_pass_update.html')

    proc = 'uspSetChannelUserPassUpdate @ChannelUserID=?, @UserPassword=?'
    conn.execute_without_return(proc, [user_id, new_passwd])

    flash("암호가 정상적으로 수정되었습니다.", category="info")
    return redirect(url_for('homes.index'))


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
    user_name = request.form.get('user_name')
    user_passwd = request.form.get('user_passwd')

    proc = 'uspSetChannelUserEmailReAuthRequest @UserEmail=?, @UserPassword=?, @UserName=?, @AuthCode=?'
    params = [user_email, user_passwd, user_name, auth_code]
    res = conn.execute_return(proc, params)[0]

    if not res:
        flash("등록된 계정이 아닙니다. 다시 확인해 해주세요.", category="danger")
        return render_template('accounts/auth_mail_resend.html', user_email=user_email, user_name=user_name)

    send_mail(user_email, user_name, auth_code, 're_auth')
    flash("인증 메일이 재발송 완료되었습니다. 개인 메일을 확인해주세요.", category="success")
    return redirect(url_for('homes.index'))


@bp.route('/user_pass_reset', methods=['GET'])
def user_pass_reset():
    if session.get('login_user'):
        return redirect(url_for('homes.index'))

    return render_template('accounts/user_pass_reset.html')


@bp.route('/user_pass_reset', methods=['POST'])
def user_pass_reset_post():
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789'
    auth_code = "".join(random.choice(alphabet) for _ in range(4))

    user_email = request.form.get('user_email')
    user_name = request.form.get('user_name')

    proc = 'uspSetChannelUserPassReset @UserEmail=?, @UserName=?, @AuthCode=?'
    params = [user_email, user_name, auth_code]
    res = conn.execute_return(proc, params)[0]

    if not res:
        flash("등록된 계정이 아닙니다. 다시 확인해 해주세요.", category="danger")
        return render_template('accounts/user_pass_reset.html', user_email=user_email, user_name=user_name)

    send_mail(user_email, user_name, auth_code, 'reset_passwd')
    flash("비밀번호 초기화 신청이 완료되었습니다. 개인 메일을 확인해 해주세요.", category="success")
    return redirect(url_for('homes.index'))


# 발송된 메일에서 확인하는 경로
@bp.route('/auth', methods=['GET'])
def auth():
    user_email = request.args.get('user_email')
    auth_code = request.args.get('auth_code')

    proc = 'uspSetChannelUserEmailAuth @UserEmail=?, @AuthCode=?'
    res = int(conn.execute_return(proc, [user_email, auth_code])[0])

    if res == 1:
        flash("이메일 인증이 완료되었습니다. 로그인 해주세요.", category="success")
        return redirect(url_for('accounts.login'))
    else:
        flash("인증에 실패했습니다. 다시 진행해 주세요.", category="danger")
        return redirect(url_for('accounts.login'))


# 발송된 메일에서 확인하는 경로
@bp.route('/auth_pass_update', methods=['GET'])
def auth_pass_update():
    user_email = request.args.get('user_email')
    auth_code = request.args.get('auth_code')

    proc = 'uspSetChannelUserPassAuth @UserEmail=?, @AuthCode=?'
    res = int(conn.execute_return(proc, [user_email, auth_code])[0])

    if res == 1:
        flash("이메일 인증이 완료되었습니다. 비밀번호를 변경해 주세요.", category="success")
        return render_template('accounts/auth_pass_update.html', user_email=user_email)
    else:
        flash("인증에 실패했습니다. 다시 진행해 주세요.", category="danger")
        return redirect(url_for('accounts.login'))



@bp.route('/auth_pass_update', methods=['POST'])
def auth_pass_update_post():
    user_email = request.form.get('user_email')
    new_passwd = request.form.get('new_passwd')
    confirm_passwd = request.form.get('confirm_passwd')

    if new_passwd != confirm_passwd:
        flash("입력한 암호가 서로 일치하지 않습니다.", category="danger")
        return render_template('accounts/auth_pass_update.html', user_email=user_email)

    proc = 'uspSetChannelUserPassAuthUpdate @UserEmail=?, @UserPassword=?'
    res = int(conn.execute_return(proc, [user_email, new_passwd])[0])

    if not res:
        flash("이메일 계정이 올바르지 않습니다. 변경 요청 절차를 다시 진행해주세요.", category="danger")
        return render_template('accounts/auth_pass_update.html', user_email=user_email)

    flash("암호가 정상적으로 수정되었습니다.", category="info")
    return redirect(url_for('accounts.login'))
