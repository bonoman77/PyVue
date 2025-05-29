import os
import random
import channel_manager.dbconns as conn
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import Blueprint, request, session, render_template, redirect, url_for, flash, jsonify
from channel_manager.utils.auth_handler import admin_required
from channel_manager.utils.page_handler import paged_list
from channel_manager.utils.file_handler import FileHandler

bp = Blueprint('admins', __name__)

@bp.route("/user_list/<int:channel_id>", methods=['GET'])
@admin_required
def user_list(channel_id):

    res_list = conn.return_list('uspGetChannelAdminUserList', None)

    return render_template('admins/user_list.html', res_list=res_list, channel_id=channel_id)


@bp.route('/set_user_status_update', methods=['POST'])
@admin_required
def set_user_status_update():
    data = request.json
    user_id = data.get('user_id')
    bool_yn = data.get('bool_yn')
    column = data.get('column')

    try:
        params = [user_id, bool_yn, column]
        conn.execute_without_return('uspSetChannelAdminUserStatusUpdate @ChannelUserID=?, @BoolYn=?, @Column=?', params)
        
        return jsonify({'success': True, 'message': 'User status updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route("/notice_list/<int:channel_id>", methods=['GET'])
@admin_required
def notice_list(channel_id):
    print(channel_id)
    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=3)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
  
    params = [search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelAdminNoticeTotalCnt @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelAdminNoticeList @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('admins/notice_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)


@bp.route('/set_notice_status_update', methods=['POST'])
@admin_required
def notice_status_update():
    data = request.json
    channel_notice_id = data.get('channel_notice_id')
    bool_yn = data.get('bool_yn')
    column = data.get('column')

    try:
        params = [channel_notice_id, bool_yn, column]
        conn.execute_without_return('uspSetChannelAdminNoticeStatusUpdate @ChannelNoticeID=?, @BoolYn=?, @Column=?', params)
        
        return jsonify({'success': True, 'message': 'User status updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@bp.route('/notice_modify/<int:channel_id>/<int:channel_notice_id>', methods=['GET'])
@admin_required
def notice_modify(channel_id, channel_notice_id):
    if channel_notice_id: 
        res = conn.execute_return("uspGetChannelNoticeDetail @ChannelNoticeID=?", channel_notice_id)
        return render_template('admins/notice_modify.html', channel_id=channel_id, channel_notice_id=channel_notice_id, res=res)

    return render_template('admins/notice_modify.html', channel_id=channel_id, channel_notice_id=channel_notice_id)


@bp.route('/notice_modify', methods=['POST'])
@admin_required
def notice_modify_post():
    user_id = session['login_user']['user_id']
    channel_id = int(request.form.get('channel_id') or 1)
    channel_notice_id = int(request.form.get('channel_notice_id') or 0)
    title = request.form.get("title")
    contents = request.form.get("contents")
    top_expose_yn = '1' if request.form.get("top_expose_yn") else '0'

    if channel_notice_id: 
        params = [channel_notice_id, user_id, title, contents, top_expose_yn]
        conn.execute_without_return("uspSetChannelNoticeUpdate @ChannelNoticeID=?, @ChannelUserID=?, @Title=?, @Contents=?, @TopExposeYn=?", params)
    else: 
        params = [user_id, title, contents, top_expose_yn]
        conn.execute_without_return("uspSetChannelNoticeInsert @ChannelUserID=?, @Title=?, @Contents=?, @TopExposeYn=?", params)

    return redirect(url_for('admins.notice_list', channel_id=channel_id))


@bp.route("/set_notice_delete", methods=['POST'])
@admin_required
def set_notice_delete():
    channel_notice_id = request.form.get('channel_notice_id')
    proc = 'uspSetChannelNoticeDelete @ChannelNoticeID=?'
    conn.execute_without_return(proc, channel_notice_id)

    return jsonify({"result": "success"})


@bp.route("/report_list/<int:channel_id>", methods=['GET'])
@admin_required
def report_list(channel_id):
    res_list = conn.return_list('uspGetChannelAdminEmailReportList', None)
    return render_template('admins/report_list.html', res_list=res_list, channel_id=channel_id)


@bp.route('/report_modify/<int:channel_id>/<int:channel_report_id>', methods=['GET'])
@admin_required
def report_modify(channel_id, channel_report_id):
    report_kind = conn.return_list("uspGetChannelCommonList @Separate=?", 'ReportKindID')

    if channel_report_id: 
        res = conn.execute_return("uspGetChannelAdminEmailReportDetail @ChannelReportID=?", channel_report_id)
        report_kind = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ReportKindID} for item in report_kind]

        return render_template('admins/report_modify.html', channel_id=channel_id, channel_report_id=channel_report_id, report_kind=report_kind, res=res)

    return render_template('admins/report_modify.html', channel_id=channel_id, channel_report_id=channel_report_id, report_kind=report_kind)


@bp.route('/report_modify', methods=['POST'])
@admin_required
def report_modify_post():
    user_id = session['login_user']['user_id']
    channel_id = int(request.form.get('channel_id') or 1)
    channel_report_id = int(request.form.get('channel_report_id') or 0)
    title = request.form.get("title")
    contents = request.form.get("contents")
    recipients = request.form.get("recipients")
    report_kind_id = request.form.get("report_kind_id")

    if channel_report_id: 
        params = [channel_report_id, user_id, title, contents, report_kind_id, recipients]
        conn.execute_without_return("uspSetChannelAdminEmailReportUpdate @ChannelReportID=?, @ChannelUserID=?, @Title=?, @Contents=?, @ReportKindID=?, @Recipients=?", params)
    else: 
        params = [user_id, title, contents, report_kind_id, recipients]
        conn.execute_without_return("uspSetChannelAdminEmailReportInsert @ChannelUserID=?, @Title=?, @Contents=?, @ReportKindID=?, @Recipients=?", params)

    return redirect(url_for('admins.report_list', channel_id=channel_id))


@bp.route('/set_report_status_update', methods=['POST'])
@admin_required
def set_report_status_update():
    data = request.json
    report_id = data.get('report_id')
    bool_yn = data.get('bool_yn')
    column = data.get('column')

    try:
        params = [report_id, bool_yn, column]
        conn.execute_without_return('uspSetChannelAdminEmailReportStatusUpdate @ChannelReportID=?, @BoolYn=?, @Column=?', params)
        
        return jsonify({'success': True, 'message': 'User status updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400
