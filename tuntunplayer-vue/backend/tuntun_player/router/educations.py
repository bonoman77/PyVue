import random
import tuntun_player.dbconns as conn
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, url_for, jsonify
from tuntun_player.utils.auth_handler import login_required, admin_required

bp = Blueprint('educations', __name__)

@bp.route("/edu_main_list/<int:class_type_id>", methods=['GET'])
@login_required
def edu_main_list(class_type_id):
    member_id = session['login_user']['member_id']

    proc = 'uspGetStreamClassGroupList @MemberID=?, @ClassTypeID=?'
    res_list = conn.return_list(proc, [member_id, class_type_id])
    return render_template('educations/edu_main_list.html', class_type_id=class_type_id, res_list=res_list)


@bp.route("/edu_info", methods=['GET'])
@login_required
def edu_info():
    class_group_id = request.args.get('class_group_id')

    proc = 'uspGetStreamClassPartialList @ClassGroupID=?'
    res_list = conn.return_list(proc, class_group_id)
    serialized_data = [{'class_id': res[0], 'class_name': res[1]} for res in res_list]

    return jsonify({"result": "success", "data": serialized_data})


@bp.route("/edu_class_attend", methods=['POST'])
@login_required
def edu_class_attend():
    member_id = session['login_user']['member_id']
    class_group_id = request.form.get('class_group_id')

    proc = "uspSetStreamClassAttendApply @MemberID=?, @ClassGroupID=?"
    conn.execute_without_return(proc, [member_id, class_group_id])

    return jsonify({"result": "success"})


@bp.route("/edu_class_view_check", methods=['POST'])
@login_required
def edu_class_view_check():
    class_id = request.form.get('class_id')
    class_attend_id = request.form.get('class_attend_id')

    proc = 'uspSetStreamClassAttendCheck @ClassID=?, @ClassAttendID=?'
    conn.execute_without_return(proc, [class_id, class_attend_id])

    return jsonify({"result": "success"})


@bp.route("/edu_list/<int:class_group_id>", methods=['GET'])
@login_required
def edu_list(class_group_id):
    member_id = session['login_user']['member_id']

    proc = 'uspGetStreamClassGroupInfo @ClassGroupID=?'
    res = conn.execute_return(proc, class_group_id)

    proc_list = 'uspGetStreamClassList @MemberID=?, @ClassGroupID=?'
    res_list = conn.return_list(proc_list, [member_id, class_group_id])

    return render_template('educations/edu_list.html', res_list=res_list, res=res)


@bp.route("/admin_edu_list")
@admin_required
def admin_edu_list():
    model_num = random.choice(range(1, 10))
    model_path = f"/static/images/notice/illust_{model_num}.png"

    return render_template('educations/admin_edu_list.html', model_path=model_path)

