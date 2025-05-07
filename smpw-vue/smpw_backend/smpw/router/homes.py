import random
from datetime import datetime
import smpw.dbconns as conn
from smpw.utils.auth_handler import login_required
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, url_for, jsonify

bp = Blueprint('homes', __name__)

@bp.route("/")
def index():
    current_datetime = datetime.now()
    set_date = current_datetime.strftime('%Y-%m-%d')
    res = conn.execute_return('uspGetStreamModalNoticeDetail @SetDate=?', set_date)

    return render_template('homes/index.html', res=res)


@bp.route("/privacy")
def privacy():
    return render_template('homes/privacy.html')


@bp.route("/term")
def term():
    return render_template('homes/term.html')


@bp.route("/term_update")
def term_update():
    return render_template('homes/term_update.html')


@bp.route("/term_teacher")
def term_teacher():
    return render_template('homes/term_teacher.html')


@bp.route("/term_teacher_update")
def term_teacher_update():
    return render_template('homes/term_teacher_update.html')


@bp.route("/native_service")
@login_required
def native_service():
    member_id = session['login_user']['member_id']
    proc = "uspGetStreamMemberApiCode @MemberID=?"
    api_code = conn.execute_return(proc, member_id).ApiCode

    return render_template('homes/native_service.html', member_id=member_id, api_code=api_code)


@bp.route("/native_service_return")
def native_service_return():
    member_id = request.args.get('memberId')
    api_code = request.args.get('apiCode')

    proc = "uspGetStreamMemberInfo @MemberID=?, @ApiCode=?"
    res = conn.execute_return(proc, [member_id, api_code])

    if res:
        response_data = {
            "name": res.MemberName,
            "eng_name": res.MemberEngName,
            "mail": res.UserEmail,
            "mobile1": res.Mobile1,
            "mobile2": res.Mobile2,
            "mobile3": res.Mobile3,
            "result": "success",
        }
    else:
        response_data = {"result": "fail"}

    return jsonify(response_data)


@bp.route("/Account/MemberInfo")  # 6월에 삭제 예정
def native_service_return_temp():
    member_id = request.args.get('memberId')
    api_code = request.args.get('apiCode')

    proc = "uspGetStreamMemberInfo @MemberID=?, @ApiCode=?"
    res = conn.execute_return(proc, [member_id, api_code])

    if res:
        response_data = {
            "name": res.MemberName,
            "eng_name": res.MemberEngName,
            "mail": res.UserEmail,
            "mobile1": res.Mobile1,
            "mobile2": res.Mobile2,
            "mobile3": res.Mobile3,
            "success": True,
        }
    else:
        response_data = {"result": False}

    return jsonify(response_data)


@bp.route("/message")
def message():
    msg_kind = request.args.get('msg_kind')
    model_num = random.randint(1, 9)
    model_path = f"/static/images/notice/illust_{model_num}.png"

    return render_template('homes/message.html', model_path=model_path, msg_kind=msg_kind)

