import os
import channel_manager.dbconns as conn
from flask import Blueprint, current_app, request, session, render_template, redirect, url_for, flash, jsonify, send_file
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from channel_manager.enums import ChannelKind, RecordKind
from channel_manager.utils.auth_handler import login_required
from channel_manager.utils.page_handler import paged_list
from channel_manager.utils.file_handler import FileHandler, excel_export_handle

bp = Blueprint('manages', __name__)


@bp.route("/promo_list/<int:channel_id>", methods=['GET'])
@login_required
def promo_list(channel_id):
    res_list = conn.return_list('uspGetChannelPromoList @ChannelKindID=?', channel_id)
    return render_template('manages/promo_list.html', res_list=res_list, channel_id=channel_id)


@bp.route('/promo_modify/<int:channel_id>/<int:channel_promo_id>', methods=['GET'])
@login_required
def promo_modify(channel_id, channel_promo_id):
    promo_kind = conn.return_list("uspGetChannelKindCommonList @ChannelKindID=?, @Separate=?", [channel_id, 'PromoKindID'])
    promo_sub_kind = conn.return_list("uspGetChannelKindCommonList @ChannelKindID=?, @Separate=?", [channel_id, 'PromoSubKindID'])
    promo_target = conn.return_list("uspGetChannelCommonList @Separate=?", 'PromoTargetID')

    today = datetime.today()

    if channel_promo_id: 
        res = conn.execute_return("uspGetChannelPromoDetail @ChannelPromoID=?", channel_promo_id)
        promo_kind = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.PromoKindID} for item in promo_kind]
        promo_sub_kind = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.PromoSubKindID} for item in promo_sub_kind]
        promo_target =  conn.return_list("uspGetChannelPromoTargetCheckList @ChannelPromoID=?", channel_promo_id) 
        file_list = conn.return_list("uspGetChannelPromoFileList @ChannelPromoID=?", channel_promo_id)

        return render_template('manages/promo_modify.html'
        , today=today
        , channel_id=channel_id
        , channel_promo_id=channel_promo_id
        , res=res
        , promo_kind=promo_kind
        , promo_sub_kind=promo_sub_kind
        , promo_target=promo_target
        , file_list=file_list)

    return render_template('manages/promo_modify.html'
    , today=today
    , channel_id=channel_id
    , channel_promo_id=channel_promo_id
    , promo_kind=promo_kind
    , promo_sub_kind=promo_sub_kind
    , promo_target=promo_target) 


@bp.route('/promo_modify', methods=['POST'])
@login_required
def promo_modify_post():
    user_id = session['login_user']['user_id']
    channel_id = int(request.form.get('channel_id') or 1)
    channel_promo_id = int(request.form.get('channel_promo_id') or 0)

    title = request.form.get("title")
    start_date = request.form.get("start_date") 
    end_date = request.form.get("end_date") or None
    promo_kind_id = request.form.get("promo_kind_id")
    promo_sub_kind_id = request.form.get("promo_sub_kind_id")
    expect_comment = request.form.get("expect_comment")
    result_comment = request.form.get("result_comment")
    promo_target_ids = '||'.join(request.form.getlist("promo_target_id"))

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Promotion')
    upload_files = request.files.getlist('upload_file_path')
    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    if channel_promo_id: 
        params = [channel_promo_id, user_id
            , title, promo_kind_id, promo_sub_kind_id, start_date, end_date
            , expect_comment, result_comment, promo_target_ids
            , upload_path, file_name_str]
        conn.execute_without_return(
            "uspSetChannelPromoUpdate @ChannelPromoID=?, @ChannelUserID=? "
            ", @Title=?, @PromoKindID=?, @PromoSubKindID=?, @StartDate=?, @EndDate=? "
            ", @ExpectComment=?, @ResultComment=?, @TargetString=? " 
            ", @UploadFilePath=?, @FileNameString=?",  
            params
        )
    else: 
        params = [user_id, channel_id
            , title, promo_kind_id, promo_sub_kind_id, start_date, end_date
            , expect_comment, result_comment, promo_target_ids
            , upload_path, file_name_str]

        conn.execute_without_return(
            "uspSetChannelPromoInsert @ChannelUserID=?, @ChannelKindID=? "
            ", @Title=?, @PromoKindID=?, @PromoSubKindID=?, @StartDate=?, @EndDate=? "
            ", @ExpectComment=?, @ResultComment=?, @TargetString=?"
            ", @UploadFilePath=?, @FileNameString=?",  
            params
        )

    return redirect(url_for('manages.promo_list', channel_id=channel_id))


@bp.route("/set_promo_delete", methods=['POST'])
@login_required
def set_promo_delete():
    channel_promo_id = request.form.get('channel_promo_id')
    proc = 'uspSetChannelPromoDelete @ChannelPromoID=?'
    conn.execute_without_return(proc, channel_promo_id)

    return jsonify({"result": "success"})


@bp.route("/set_promo_file_delete", methods=['POST'])
@login_required
def set_promo_file_delete():
    promo_file_id = request.form.get('promo_file_id')
    user_id = session['login_user']['user_id']
    proc = 'uspSetChannelPromoFileDelete @ChannelPromoFileID=?, @DeleteChannelUserID=?'
    conn.execute_without_return(proc, [promo_file_id, user_id])

    return jsonify({"result": "success"})


@bp.route("/goal_list/<int:channel_id>", methods=['GET'])
@login_required
def goal_list(channel_id):
    res_list = conn.return_list('uspGetChannelGoalList @ChannelKindID=?', channel_id)
    return render_template('manages/goal_list.html', res_list=res_list, channel_id=channel_id)


@bp.route('/goal_modify/<int:channel_id>/<int:channel_goal_id>', methods=['GET'])
@login_required
def goal_modify(channel_id, channel_goal_id):
    goal_kind = conn.return_list("uspGetChannelCommonList @Separate=?", 'GoalKindID')
    goal_group = conn.return_list("uspGetChannelKindCommonList @ChannelKindID=?, @Separate=?", [channel_id, 'GoalGroupID'])

    next_month = datetime.today() + relativedelta(months=1)

    if channel_goal_id: 
        res = conn.execute_return("uspGetChannelGoalDetail @ChannelGoalID=?", channel_goal_id)
        res_list = conn.return_list("uspGetChannelGoalDetailAmount @ChannelKindID=?, @ChannelGoalID=?", [channel_id, channel_goal_id])

        return render_template('manages/goal_modify.html'
        , next_month=next_month
        , channel_id=channel_id
        , channel_goal_id=channel_goal_id
        , res=res
        , res_list=res_list
        , goal_kind=goal_kind
        , goal_group=goal_group
        )

    return render_template('manages/goal_modify.html'
    , next_month=next_month
    , channel_id=channel_id
    , channel_goal_id=channel_goal_id
    , goal_kind=goal_kind
    , goal_group=goal_group
    ) 


@bp.route('/goal_modify', methods=['POST'])
@login_required
def goal_modify_post():
    user_id = session['login_user']['user_id']
    channel_id = int(request.form.get('channel_id') or 1)
    channel_goal_id = int(request.form.get('channel_goal_id') or 0)
    goal_month = request.form.get("goal_month") + '-01'
    goal_kind_id = request.form.get("goal_kind_id")

    if channel_goal_id: 
        params = [channel_goal_id, user_id, goal_kind_id, goal_month] 
        conn.execute_without_return(
            "uspSetChannelGoalUpdate @ChannelGoalID=?, @ChannelUserID=?, @GoalKindID=?, @GoalMonth=? ", params 
        )
    else: 
        params = [channel_id, goal_kind_id, goal_month] 
        channel_goal_yn = conn.execute_return(
            "uspGetChannelGoalExistConfirm @ChannelKindID=?, @GoalKindID=?, @GoalMonth=? ", params 
        ).ChannelGoalYn 

        if channel_goal_yn: 
            flash("같은 년월에 이미 등록된 목표값이 있습니다.", category="danger")
            return redirect(url_for('manages.goal_list', channel_id=channel_id))

        params = [user_id, channel_id, goal_kind_id, goal_month] 
        channel_goal_id = conn.execute_return(
            "uspSetChannelGoalInsert @ChannelUserID=?, @ChannelKindID=?, @GoalKindID=?, @GoalMonth=? ", params 
        ).ChannelGoalID

    goal_group = conn.return_list("uspGetChannelKindCommonList @ChannelKindID=?, @Separate=?", [channel_id, 'GoalGroupID'])

    for g in goal_group:
        params = [channel_goal_id, g.ID, request.form.get(str(g.ID)) or 0] 
        conn.execute_without_return(
            "uspSetChannelGoalAmountSet @ChannelGoalID=?, @GoalGroupID=?, @Amount=? ", params 
        )

    return redirect(url_for('manages.goal_list', channel_id=channel_id))


@bp.route("/set_goal_delete", methods=['POST'])
@login_required
def set_goal_delete():
    channel_goal_id = request.form.get('channel_goal_id')
    proc = 'uspSetChannelGoalDelete @ChannelGoalID=?'
    conn.execute_without_return(proc, channel_goal_id)

    return jsonify({"result": "success"})


