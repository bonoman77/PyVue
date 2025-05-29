import random
from datetime import datetime
import channel_manager.dbconns as conn
from channel_manager.utils.auth_handler import login_required
from flask import Blueprint, request, session, render_template, redirect, url_for, flash, json, jsonify

bp = Blueprint('homes', __name__)

@bp.route("/", methods=['GET'])
@bp.route("/<int:channel_id>", methods=['GET'])
@login_required
def index(channel_id=None):
    if channel_id is None:
        channel_id = session.get('login_user', {}).get('channel_id', 1)

    res = conn.execute_return('uspGetChannelDashboardCounselCnt @ChannelKindID=?', channel_id)
    notice_list = conn.return_list('uspGetChannelNoticeMainList')
    res_list = conn.return_list('uspGetChannelAgencyList @ChannelKindID=?', channel_id)
    return render_template('homes/index.html', res=res, res_list=res_list, notice_list=notice_list, channel_id=channel_id)


@bp.route("/privacy")
def privacy():
    return render_template('homes/privacy.html')


@bp.route("/term")
def term():
    return render_template('homes/term.html')


@bp.route("/version_history/<int:channel_id>", methods=['GET'])
@login_required
def version_history(channel_id):
    return render_template('homes/version_history.html', channel_id=channel_id)


@bp.route("/message")
def message():
    msg_kind = request.args.get('msg_kind')
    model_num = random.randint(1, 9)
    model_path = f"/static/images/notice/illust_{model_num}.png"

    return render_template('homes/message.html', model_path=model_path, msg_kind=msg_kind)

@bp.route("/notice_list/<int:channel_id>", methods=['GET'])
@login_required
def notice_list(channel_id):
    res_list = conn.return_list('uspGetChannelNoticeSubList')

    return render_template('homes/notice_list.html', res_list=res_list, channel_id=channel_id)


@bp.route('/get_notice_content', methods=['GET'])
@login_required
def get_notice_content():
    channel_notice_id = request.args.get('channel_notice_id')
    
    try:
        res = conn.execute_return('uspGetChannelNoticeDetail @ChannelNoticeID=?', channel_notice_id)
        
        if res:
            return jsonify({'content': res.Contents}), 200
        else:
            return jsonify({'error': '공지를 찾을 수 없습니다.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500