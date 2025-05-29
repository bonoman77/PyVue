import os
import openpyxl
import channel_manager.dbconns as conn
from flask import Blueprint, request, session, render_template, redirect, url_for, flash, jsonify, send_file
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from channel_manager.enums import ChannelKind
from channel_manager.utils.auth_handler import login_required, admin_required
from channel_manager.utils.page_handler import paged_list
from channel_manager.utils.file_handler import FileHandler, excel_export_handle

bp = Blueprint('sources', __name__)

@bp.route("/experience_list/<int:channel_id>", methods=['GET'])
@login_required
def experience_list(channel_id):
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSourceExperienceExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '이름', '생년', '연락처', '주소', '교육본부', '접수일', '접수수단', '유입경로']]
        for item in res_list:
            excel_data.append([
                item.SourceID, 
                item.RegistrantName, 
                item.BirthYear,
                item.Mobile, 
                item.RegistrantAddress, 
                item.AgencyName, 
                item.ReceiptDate,
                item.InflowRoute,  
                item.ContactRoute 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'source_experience_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


    partner_list = conn.return_list("uspGetChannelAgencyList @ChannelKindId=?", channel_id)

    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSourceExperienceTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSourceExperienceList @ChannelKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('sources/experience_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search, partner_list=partner_list)


@bp.route("/internal_list/<int:channel_id>", methods=['GET'])
@login_required
def internal_list(channel_id):
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSourceExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '이름', '생년', '연락처', '교육본부', '접수일', '접수수단', '추천교사']]
        for item in res_list:
            excel_data.append([
                item.SourceID, 
                item.RegistrantName, 
                item.BirthYear,
                item.Mobile, 
                item.AgencyName, 
                item.ReceiptDate,
                item.InflowRoute,  
                item.RecommendTeacher 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'source_internal_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSourceTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSourceList @ChannelKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('sources/internal_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)


@bp.route("/level_test_list/<int:channel_id>", methods=['GET'])
@login_required
def level_test_list(channel_id):
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSourceLevelTestExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '이름', '생년월일', '연락처', '등록일']]
        for item in res_list:
            excel_data.append([
                item.SourceID, 
                item.RegistrantName, 
                item.BirthDate,
                item.Mobile,
                item.CreateDate, 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'source_level_test_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSourceLevelTestTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSourceLevelTestList @ChannelKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('sources/level_test_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)


@bp.route("/moms_class_list/<int:channel_id>", methods=['GET'])
@login_required
def moms_class_list(channel_id):
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSourceMomClassExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '이름', '생년/월', '학부모이름', '연락처', '주소', '회원여부', '추천센터', '신청센터', '등록일']]
        for item in res_list:
            excel_data.append([
                item.ApplyID, 
                item.ChildName, 
                item.ChildBirth,
                item.ParentName, 
                item.ParentMobile, 
                item.Addr, 
                item.MemberYn,
                item.RecommendAgency,  
                item.AgencyName,     
                item.CreateDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'source_mom_class_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSourceMomClassTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt
    print(total)
    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSourceMomClassList @ChannelKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('sources/moms_class_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)


@bp.route("/event_list/<int:channel_id>/<int:source_type_id>", methods=['GET'])
@login_required
def event_list(channel_id, source_type_id):
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, source_type_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSourceSeasonalExcelList @ChannelKindID=?, @SourceTypeID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '이름', '나이', '연락처', '주소', '소스종류', '프리미엄', '접수일']]
        for item in res_list:
            excel_data.append([
                item.SourceID, 
                item.RegistrantName, 
                item.Age,
                item.Mobile, 
                item.RegistrantAddress, 
                item.SourceKind, 
                item.PremiumYn, 
                item.ReceiptDate,
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'source_seasonal_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [channel_id, source_type_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSourceSeasonalTotalCnt @ChannelKindID=?, @SourceTypeID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, source_type_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSourceSeasonalList @ChannelKindID=?, @SourceTypeID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('sources/event_list.html', res_list=res_list, channel_id=channel_id, source_type_id=source_type_id, paging=paging, search=search)


@bp.route("/reward_list/<int:channel_id>", methods=['GET'])
@login_required
def reward_list(channel_id):
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, 90, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSourceSeasonalExcelList @ChannelKindID=?, @SourceTypeID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '이름', '나이', '연락처', '주소', '소스종류', '유효성', '교육본부', '접수일']]
        for item in res_list:
            excel_data.append([
                item.SourceID, 
                item.RegistrantName, 
                item.Age,
                item.Mobile, 
                item.RegistrantAddress, 
                item.SourceKind, 
                item.ValidYn, 
                item.AgencyName,
                item.ReceiptDate,  
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'source_reward_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    partner_list = conn.return_list("uspGetChannelAgencyList @ChannelKindId=?", channel_id)

    params = [channel_id, 90, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSourceSeasonalTotalCnt @ChannelKindID=?, @SourceTypeID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, 90, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSourceSeasonalList @ChannelKindID=?, @SourceTypeID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('sources/reward_list.html', res_list=res_list, channel_id=channel_id, partner_list=partner_list, paging=paging, search=search)


@bp.route("/fair_list/<int:channel_id>", methods=['GET'])
@login_required
def fair_list(channel_id):
    start_date = request.args.get('start_date', date.today().replace(day=1).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSourceFairExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '이름', '생년', '연락처', '주소', '교육본부', '접수일', '접수수단', '유입경로']]
        for item in res_list:
            excel_data.append([
                item.SourceID, 
                item.RegistrantName, 
                item.BirthYear,
                item.Mobile, 
                item.RegistrantAddress, 
                item.AgencyName, 
                item.ReceiptDate,
                item.InflowRoute,  
                item.ContactRoute 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'source_fair_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSourceFairTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSourceFairList @ChannelKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('sources/fair_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)


@bp.route('/set_source_partner_update', methods=['POST'])
@login_required
def set_source_partner_update():
    channel_id = request.form.get('channel_id')
    partner_code = request.form.get('partner_code')
    source_list = request.form.get('source_list')

    params = [channel_id, partner_code, source_list]
    print(params)
    conn.execute_without_return('uspSetChannelSourceAgencyUpdate @ChannelKindID=?, @AgencyCode=?, @SourceItemString=?', params)

    return jsonify({"result": "success"})


@bp.route('/set_source_status_update', methods=['POST'])
@admin_required
def set_source_status_update():
    data = request.json
    source_id = data.get('source_id')
    bool_yn = data.get('bool_yn')
    column = data.get('column')

    try:
        params = [source_id, bool_yn, column]
        conn.execute_without_return('uspSetChannelSourceStatusUpdate @SourceID=?, @BoolYn=?, @Column=?', params)
        
        return jsonify({'success': True, 'message': 'User status updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400