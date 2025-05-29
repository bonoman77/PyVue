import os
import openpyxl
import channel_manager.dbconns as conn
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, jsonify, send_file, url_for
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from channel_manager.enums import ChannelKind, RecordKind
from channel_manager.utils.auth_handler import login_required
from channel_manager.utils.page_handler import paged_list
from channel_manager.utils.file_handler import FileHandler, excel_export_handle

bp = Blueprint('counsels', __name__)

@bp.route("/agency_list/<int:channel_id>", methods=['GET'])
@login_required
def agency_list(channel_id):
    res_list = conn.return_list('uspGetChannelAgencyList @ChannelKindID=?', channel_id)
    return render_template('counsels/agency_list.html', res_list=res_list, channel_id=channel_id)


@bp.route('/agency_map/<int:channel_id>/<int:channel_agency_id>', methods=['GET'])
@login_required
def agency_map(channel_id, channel_agency_id):
    agency = conn.execute_return("uspGetChannelAgencyDetail @ChannelKindID=?, @ChannelAgencyID=?", [channel_id, channel_agency_id])

    return render_template('counsels/agency_map.html', channel_id=channel_id, agency=agency)    


@bp.route("/agency_consult_list/<int:channel_id>/<int:channel_agency_id>", methods=['GET'])
@login_required
def agency_consult_list(channel_id, channel_agency_id):
    export_yn = request.args.get('export_yn', False)
    if export_yn: 
        params = [channel_id, channel_agency_id]
        res_list = conn.return_list('uspGetChannelConsultAgencyExcelList @ChannelKindID=?, @ChannelAgencyID=?', params)

        excel_data = [['No.', '파트너코드', '파트너명', '카테고리', '제목', '내용', '피상담자', '작성자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.AgencyCode, 
                item.AgencyName, 
                item.CategoryName, 
                item.Title,
                item.Contents, 
                item.Contacter,
                item.UserName,  
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'agency_consult_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    res = conn.execute_return('uspGetChannelAgencyName @ChannelAgencyID=?', channel_agency_id)
    res_list = conn.return_list('uspGetChannelConsultAgencyList @ChannelKindID=?, @ChannelAgencyID=?', [channel_id, channel_agency_id])
    return render_template('counsels/agency_consult_list.html', channel_id=channel_id, res=res, res_list=res_list)


@bp.route("/agency_support_list/<int:channel_id>/<int:channel_agency_id>", methods=['GET'])
@login_required
def agency_support_list(channel_id, channel_agency_id):
    export_yn = request.args.get('export_yn', False)
    if export_yn: 
        params = [channel_id, channel_agency_id]
        res_list = conn.return_list('uspGetChannelSupportAgencyExcelList @ChannelKindID=?, @ChannelAgencyID=?', params)

        excel_data = [['No.', '파트너코드', '파트너명', '카테고리', '지원수량', '지원금액', '제목', '내용', '작성자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.AgencyCode, 
                item.AgencyName, 
                item.CategoryName, 
                f"{item.SupportQty:,}",
                f"{item.SupportAmt:,}",
                item.Title,
                item.Contents, 
                item.UserName,  
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'agency_support_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    res = conn.execute_return('uspGetChannelAgencyName @ChannelAgencyID=?', channel_agency_id)
    res_list = conn.return_list('uspGetChannelSupportAgencyList @ChannelKindID=?, @ChannelAgencyID=?', [channel_id, channel_agency_id])
    return render_template('counsels/agency_support_list.html', channel_id=channel_id, res=res, res_list=res_list)


@bp.route("/agency_violation_list/<int:channel_id>/<int:channel_agency_id>", methods=['GET'])
@login_required
def agency_violation_list(channel_id, channel_agency_id):
    export_yn = request.args.get('export_yn', False)
    if export_yn: 
        params = [channel_id, channel_agency_id]
        res_list = conn.return_list('uspGetChannelViolationAgencyExcelList @ChannelKindID=?, @ChannelAgencyID=?', params)

        excel_data = [['No.', '파트너코드', '파트너명', '카테고리', '제목', '내용', '작성자', '동행자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.AgencyCode, 
                item.AgencyName, 
                item.CategoryName, 
                item.Title,
                item.Contents, 
                item.UserName,  
                item.CompanionName,
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'agency_support_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    res = conn.execute_return('uspGetChannelAgencyName @ChannelAgencyID=?', channel_agency_id)
    res_list = conn.return_list('uspGetChannelViolationAgencyList @ChannelKindID=?, @ChannelAgencyID=?', [channel_id, channel_agency_id])
    return render_template('counsels/agency_violation_list.html', channel_id=channel_id, res=res, res_list=res_list)



@bp.route("/consult_list/<int:channel_id>", methods=['GET'])
@login_required
def consult_list(channel_id):
    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=1)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelConsultExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '파트너코드', '파트너명', '카테고리', '제목', '내용', '피상담자', '작성자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.AgencyCode, 
                item.AgencyName, 
                item.CategoryName, 
                item.Title,
                item.Contents, 
                item.Contacter,
                item.UserName,  
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'consult_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  
    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelConsultTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelConsultList @ChannelKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('counsels/consult_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)



@bp.route("/consult_total_list/<int:channel_id>", methods=['GET'])
@login_required
def consult_total_list(channel_id):
    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=1)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelConsultEveryExcelList @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '채널종류', '파트너코드', '파트너명', '카테고리', '제목', '내용', '피상담자', '작성자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.ChannelKind, 
                item.AgencyCode, 
                item.AgencyName, 
                item.CategoryName, 
                item.Title,
                item.Contents, 
                item.Contacter,
                item.UserName,  
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'consult_total_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelConsultEveryTotalCnt @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt    

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelConsultEveryList @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }

    return render_template('counsels/consult_total_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)



@bp.route('/consult_modify/<int:channel_id>/<int:channel_agency_id>/<int:channel_manage_id>', methods=['GET'])
@login_required
def consult_modify(channel_id, channel_agency_id, channel_manage_id):
    agency = conn.execute_return("uspGetChannelAgencyDetail @ChannelKindID=?, @ChannelAgencyID=?", [channel_id, channel_agency_id])
    contact_style = conn.return_list("uspGetChannelCommonList @Separate=?", 'ContactStyleID')
    contacter = conn.return_list("uspGetChannelCommonList @Separate=?", 'ContacterID')
    consult_type = conn.return_list("uspGetChannelCommonList @Separate=?", 'ConsultTypeID')
    manner_kind = conn.return_list("uspGetChannelCommonList @Separate=?", 'ContacterMannerID')

    today = datetime.today()

    if channel_manage_id: 
        res = conn.execute_return("uspGetChannelConsultDetail @ChannelManageID=?", channel_manage_id)

        contact_style = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ContactStyleID} for item in contact_style]
        contacter = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ContacterID} for item in contacter]
        consult_type = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ConsultTypeID} for item in consult_type]
        manner_kind =  conn.return_list("uspGetChannelConsultMannerCheckList @ChannelManageID=?", channel_manage_id) 
        file_list = conn.return_list("uspGetChannelManageFileList @ChannelManageID=?", channel_manage_id)

        return render_template('counsels/consult_modify.html', channel_id=channel_id, agency=agency, res=res 
        , today=today
        , channel_manage_id=channel_manage_id
        , channel_agency_id=channel_agency_id
        , contact_style=contact_style
        , contacter=contacter
        , consult_type=consult_type
        , manner_kind=manner_kind
        , file_list=file_list
        )

    return render_template('counsels/consult_modify.html', channel_id=channel_id, agency=agency
        , today=today
        , channel_agency_id=channel_agency_id
        , contact_style=contact_style
        , contacter=contacter
        , consult_type=consult_type
        , manner_kind=manner_kind
        )


@bp.route('/consult_modify', methods=['POST'])
@login_required
def consult_modify_post():
    user_id = session['login_user']['user_id']
    channel_id = int(request.form.get('channel_id') or 1)
    channel_manage_id = int(request.form.get('channel_manage_id') or 0)
    channel_agency_id = int(request.form.get('channel_agency_id') or 0)
    record_kind_id = RecordKind.CONSULT.value

    title = request.form.get("title")
    contents = request.form.get("contents")
    contact_date = request.form.get("contact_date") 
    complete_date = request.form.get("complete_date") or None
    contact_style_id = request.form.get("contact_style_id")
    consult_type_id = request.form.get("consult_type_id")
    contacter_id = request.form.get("contacter_id")
    contacter_name = request.form.get("contacter_name")
    companion_name = request.form.get("companion_name")
    manner_kind_ids = '||'.join(request.form.getlist("manner_kind_id"))

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Consult')
    upload_files = request.files.getlist('upload_file_path')
    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)


    if channel_manage_id: 
        params = [channel_manage_id, user_id
            , title, contents, contact_date, complete_date
            , contact_style_id, consult_type_id, contacter_id
            , contacter_name, companion_name, manner_kind_ids
            , upload_path, file_name_str]
        conn.execute_without_return(
            "uspSetChannelConsultUpdate @ChannelManageID=?, @ChannelUserID=? "
            ", @Title=?, @Contents=?, @ContactDate=?, @CompleteDate=? "
            ", @ContactStyleID=?, @ConsultTypeID=?, @ContacterID=? "
            ", @ContacterName=?, @CompanionName=?, @MannerString=? " 
            ", @UploadFilePath=?, @FileNameString=?",  
            params
        )
    else: 
        params = [channel_agency_id, user_id, record_kind_id
            , title, contents, contact_date, complete_date
            , contact_style_id, consult_type_id, contacter_id
            , contacter_name, companion_name, manner_kind_ids
            , upload_path, file_name_str]

        conn.execute_without_return(
            "uspSetChannelConsultInsert @ChannelAgencyID=?, @ChannelUserID=?, @RecordKindID=? "
            ", @Title=?, @Contents=?, @ContactDate=?, @CompleteDate=? "
            ", @ContactStyleID=?, @ConsultTypeID=?, @ContacterID=? "
            ", @ContacterName=?, @CompanionName=?, @MannerString=?"
            ", @UploadFilePath=?, @FileNameString=?",  
            params
        )

    return redirect(url_for('counsels.agency_consult_list', channel_id=channel_id, channel_agency_id=channel_agency_id))


@bp.route("/support_list/<int:channel_id>", methods=['GET'])
@login_required
def support_list(channel_id):
    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=1)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSupportExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '파트너코드', '파트너명', '카테고리', '지원수량', '지원금액', '제목', '내용', '작성자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.AgencyCode, 
                item.AgencyName, 
                item.CategoryName,
                f"{item.SupportQty:,}",
                f"{item.SupportAmt:,}",
                item.Title,
                item.Contents, 
                item.UserName,  
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'support_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSupportTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)

    params = [channel_id, page, row_size, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSupportList @ChannelKindID=?, @PageNumber=?, @PageSize=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }

    return render_template('counsels/support_list.html', res_list=res_list, total=total, channel_id=channel_id, paging=paging, search=search)


@bp.route("/support_total_list/<int:channel_id>", methods=['GET'])
@login_required
def support_total_list(channel_id):
    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=1)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelSupportEveryExcelList @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '채널종류', '파트너코드', '파트너명', '카테고리', '지원수량', '지원금액', '제목', '내용', '작성자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.ChannelKind,
                item.AgencyCode,
                item.AgencyName, 
                item.CategoryName, 
                f"{item.SupportQty:,}",
                f"{item.SupportAmt:,}",
                item.Title,
                item.Contents, 
                item.UserName,  
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'support_total_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelSupportEveryTotalCnt @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt
    
    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)

    params = [page, row_size, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelSupportEveryList @PageNumber=?, @PageSize=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }

    return render_template('counsels/support_total_list.html', res_list=res_list, total=total, channel_id=channel_id, paging=paging, search=search)


@bp.route('/support_modify/<int:channel_id>/<int:channel_agency_id>/<int:channel_manage_id>', methods=['GET'])
@login_required
def support_modify(channel_id, channel_agency_id, channel_manage_id):
    agency = conn.execute_return("uspGetChannelAgencyDetail @ChannelKindID=?, @ChannelAgencyID=?", [channel_id, channel_agency_id])
    contact_style = conn.return_list("uspGetChannelCommonList @Separate=?", 'ContactStyleID')
    support_kind = conn.return_list("uspGetChannelCommonList @Separate=?", 'SupportKindID')

    today = datetime.today()

    if channel_manage_id: 
        res = conn.execute_return("uspGetChannelSupportDetail @ChannelManageID=?", channel_manage_id)
        contact_style = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ContactStyleID} for item in contact_style]
        support_kind = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.SupportKindID} for item in support_kind]
        file_list = conn.return_list("uspGetChannelManageFileList @ChannelManageID=?", channel_manage_id)

        return render_template('counsels/support_modify.html', channel_id=channel_id, agency=agency, res=res
            , today=today
            , channel_manage_id=channel_manage_id 
            , channel_agency_id=channel_agency_id
            , contact_style=contact_style
            , support_kind=support_kind
            , file_list=file_list)

    return render_template('counsels/support_modify.html', channel_id=channel_id, agency=agency
        , today=today
        , channel_agency_id=channel_agency_id
        , contact_style=contact_style
        , support_kind=support_kind)


@bp.route('/support_modify', methods=['POST'])
@login_required
def support_modify_post():
    user_id = session['login_user']['user_id']
    channel_id = int(request.form.get('channel_id') or 1)
    channel_manage_id = int(request.form.get('channel_manage_id') or 0)
    channel_agency_id = int(request.form.get('channel_agency_id') or 0)
    record_kind_id = RecordKind.SUPPORT.value

    title = request.form.get("title")
    contents = request.form.get("contents")
    contact_date = request.form.get("contact_date") 
    complete_date = request.form.get("complete_date") or None
    support_qty = request.form.get("support_qty")
    support_amt = request.form.get("support_amt")

    contact_style_id = request.form.get("contact_style_id")
    support_kind_id = request.form.get("support_kind_id")
    companion_name = request.form.get("companion_name")

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Support')
    upload_files = request.files.getlist('upload_file_path')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    if channel_manage_id: 
        params = [channel_manage_id, user_id
            , title, contents, contact_date, complete_date, support_qty, support_amt
            , contact_style_id, support_kind_id, companion_name
            , upload_path, file_name_str]
        conn.execute_without_return(
            "uspSetChannelSupportUpdate @ChannelManageID=?, @ChannelUserID=? "
            ", @Title=?, @Contents=?, @ContactDate=?, @CompleteDate=?, @SupportQty=?, @SupportAmt=? "
            ", @ContactStyleID=?, @SupportKindID=?, @CompanionName=?"
            ", @UploadFilePath=?, @FileNameString=?", 
            params
        )
    else: 
        params = [channel_agency_id, user_id, record_kind_id
            , title, contents, contact_date, complete_date, support_qty, support_amt
            , contact_style_id, support_kind_id, companion_name
            , upload_path, file_name_str]
        conn.execute_without_return(
            "uspSetChannelSupportInsert @ChannelAgencyID=?, @ChannelUserID=?, @RecordKindID=? "
            ", @Title=?, @Contents=?, @ContactDate=?, @CompleteDate=?, @SupportQty=?, @SupportAmt=? "
            ", @ContactStyleID=?, @SupportKindID=?, @CompanionName=?"
            ", @UploadFilePath=?, @FileNameString=?", 
            params
        )

    return redirect(url_for('counsels.agency_support_list', channel_id=channel_id, channel_agency_id=channel_agency_id))


@bp.route("/violation_list/<int:channel_id>", methods=['GET'])
@login_required
def violation_list(channel_id):
    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=1)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [channel_id, search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelViolationExcelList @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '파트너코드', '파트너명', '카테고리', '제목', '내용', '작성자', '동행자','상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.AgencyCode,
                item.AgencyName, 
                item.CategoryName, 
                item.Title,
                item.Contents, 
                item.UserName,  
                item.CompanionName,
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'violation_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
  
    params = [channel_id, search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelViolationTotalCnt @ChannelKindID=?, @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [channel_id, row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelViolationList @ChannelKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }
    return render_template('counsels/violation_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)


@bp.route("/violation_total_list/<int:channel_id>", methods=['GET'])
@login_required
def violation_total_list(channel_id):
    start_date = request.args.get('start_date', (datetime.now().date() - relativedelta(years=1)).strftime('%m/%d/%Y'))
    end_date = request.args.get('end_date', datetime.now().date().strftime('%m/%d/%Y'))
    search_text = request.args.get('search_text', None)
    export_yn = request.args.get('export_yn', False)

    if export_yn: 
        params = [search_text, start_date, end_date]
        res_list = conn.return_list('uspGetChannelViolationEveryExcelList @SearchText=?, @StartDate=?, @EndDate=?', params)

        excel_data = [['No.', '채널종류', '파트너코드', '파트너명', '카테고리', '제목', '내용', '작성자', '동행자', '상담일', '완료일']]
        for item in res_list:
            excel_data.append([
                item.ChannelManageID, 
                item.ChannelKind, 
                item.AgencyCode, 
                item.AgencyName, 
                item.CategoryName, 
                item.Title,
                item.Contents, 
                item.UserName,  
                item.CompanionName,
                item.ContactDate, 
                item.CompleteDate 
                ]
            )

        output = excel_export_handle(excel_data)

        return send_file(output, 
                        download_name=f'violation_total_list_{datetime.now().strftime("%Y%m%d")}.xlsx',
                        as_attachment=True,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    params = [search_text, start_date, end_date]
    total = conn.execute_return('uspGetChannelViolationEveryTotalCnt @SearchText=?, @StartDate=?, @EndDate=?', params).TotalCnt    

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)
    params = [row_size, page, search_text, start_date, end_date]
    res_list = conn.return_list('uspGetChannelViolationEveryList @PageSize=?, @PageNumber=?, @SearchText=?, @StartDate=?, @EndDate=?', params)

    search = {
        'total': total, 
        'start_date': start_date,
        'end_date': end_date,
        'search_text': search_text,
    }

    return render_template('counsels/violation_total_list.html', res_list=res_list, channel_id=channel_id, paging=paging, search=search)



@bp.route('/violation_modify/<int:channel_id>/<int:channel_agency_id>/<int:channel_manage_id>', methods=['GET'])
@login_required
def violation_modify(channel_id, channel_agency_id, channel_manage_id):
    agency = conn.execute_return("uspGetChannelAgencyDetail @ChannelKindID=?, @ChannelAgencyID=?", [channel_id, channel_agency_id])
    contact_style = conn.return_list("uspGetChannelCommonList @Separate=?", 'ContactStyleID')
    violation_type = conn.return_list("uspGetChannelCommonList @Separate=?", 'ViolationTypeID')
    violation_level = conn.return_list("uspGetChannelCommonList @Separate=?", 'ViolationLevelID')
    panalty_type = conn.return_list("uspGetChannelCommonList @Separate=?", 'PanaltyTypeID')

    today = datetime.today()

    if channel_manage_id: 
        res = conn.execute_return("uspGetChannelViolationDetail @ChannelManageID=?", channel_manage_id)

        contact_style = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ContactStyleID} for item in contact_style]
        violation_type = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ViolationTypeID} for item in violation_type]
        violation_level = [{'ID': item.ID, 'Item': item.Item, 'Selected': item.ID == res.ViolationLevelID} for item in violation_level]
        panalty_type =  conn.return_list("uspGetChannelViolationPanaltyTypeCheckList @ChannelManageID=?", channel_manage_id) 
        file_list = conn.return_list("uspGetChannelManageFileList @ChannelManageID=?", channel_manage_id)

        return render_template('counsels/violation_modify.html', channel_id=channel_id, agency=agency, res=res
            , today=today
            , channel_manage_id=channel_manage_id
            , channel_agency_id=channel_agency_id
            , contact_style=contact_style
            , violation_type=violation_type
            , violation_level=violation_level
            , panalty_type=panalty_type
            , file_list=file_list)

    return render_template('counsels/violation_modify.html', channel_id=channel_id, agency=agency
        , today = datetime.today()
        , channel_agency_id=channel_agency_id
        , contact_style=contact_style
        , violation_type=violation_type
        , violation_level=violation_level
        , panalty_type=panalty_type)


@bp.route('/violation_modify', methods=['POST'])
@login_required
def violation_modify_post():
    user_id = session['login_user']['user_id']
    channel_id = int(request.form.get('channel_id') or 1)
    channel_manage_id = int(request.form.get('channel_manage_id') or 0)
    channel_agency_id = int(request.form.get('channel_agency_id') or 0)
    record_kind_id = RecordKind.VIOLATION.value

    title = request.form.get("title")
    contents = request.form.get("contents")
    contact_date = request.form.get("contact_date") 
    complete_date = request.form.get("complete_date") or None
    contact_style_id = request.form.get("contact_style_id")
    violation_type_id = request.form.get("violation_type_id")
    violation_level_id = request.form.get("violation_level_id")
    companion_name = request.form.get("companion_name")
    panalty_type_ids = '||'.join(request.form.getlist("panalty_type_id"))
    print(panalty_type_ids)

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Violation')
    upload_files = request.files.getlist('upload_file_path')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    if channel_manage_id: 
        params = [channel_manage_id, user_id
            , title, contents, contact_date, complete_date, companion_name
            , contact_style_id, violation_type_id, violation_level_id, panalty_type_ids
            , upload_path, file_name_str]
        conn.execute_without_return(
            "uspSetChannelViolationUpdate @ChannelManageID=?, @ChannelUserID=? "
            ", @Title=?, @Contents=?, @ContactDate=?, @CompleteDate=?, @CompanionName=? "
            ", @ContactStyleID=?, @ViolationTypeID=?, @ViolationLevelID=?, @PanaltyTypeString=?"
            ", @UploadFilePath=?, @FileNameString=?", 
            params
        )
    else: 
        params = [channel_agency_id, user_id, record_kind_id
            , title, contents, contact_date, complete_date, companion_name
            , contact_style_id, violation_type_id, violation_level_id, panalty_type_ids
            , upload_path, file_name_str]
        conn.execute_without_return(
            "uspSetChannelViolationInsert @ChannelAgencyID=?, @ChannelUserID=?, @RecordKindID=? "
            ", @Title=?, @Contents=?, @ContactDate=?, @CompleteDate=?, @CompanionName=? "
            ", @ContactStyleID=?, @ViolationTypeID=?, @ViolationLevelID=?, @PanaltyTypeString=?"
            ", @UploadFilePath=?, @FileNameString=?", 
            params
        )

    return redirect(url_for('counsels.agency_violation_list', channel_id=channel_id, channel_agency_id=channel_agency_id))


@bp.route("/set_manage_delete", methods=['POST'])
@login_required
def set_manage_delete():
    manage_id = request.form.get('manage_id')
    user_id = session['login_user']['user_id']
    proc = 'uspSetChannelManageDelete @ChannelManageID=?, @UpdateChannelUserID=?'
    conn.execute_without_return(proc, [manage_id, user_id])

    return jsonify({"result": "success"})


@bp.route("/set_manage_file_delete", methods=['POST'])
@login_required
def set_manage_file_delete():
    manage_file_id = request.form.get('manage_file_id')
    user_id = session['login_user']['user_id']
    proc = 'uspSetChannelManageFileDelete @ChannelManageFileID=?, @DeleteChannelUserID=?'
    conn.execute_without_return(proc, [manage_file_id, user_id])

    return jsonify({"result": "success"})


@bp.route("/set_support_upload_excel", methods=['POST'])
@login_required
def set_support_upload_excel():
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Excel')
    upload_files = request.files.getlist('upload_file_path')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    if file_name_str:
        excel_file_path = os.path.join(upload_path, file_name_str)
        workbook = openpyxl.load_workbook(excel_file_path)
        sheet = workbook.active

        # 헤더 검증
        header = [str(cell.value) if cell.value is not None else '' for cell in sheet[1]]
        if any(not h for h in header):
            error_msg = "엑셀 파일의 헤더 행에 빈 셀이 있습니다."
            return jsonify({"error": error_msg}), 400

        required_columns = ['ChannelKindName', 'AgencyCode', 'ContactStyle', 'SupportKind', 
                          'SupportQty', 'SupportAmt', 'ChannelPromoID', 'ContactDate', 
                          'CompleteDate', 'Title', 'Contents']
        
        missing_columns = [col for col in required_columns if col not in header]
        if missing_columns:
            error_msg = f"필수 컬럼이 누락되었습니다: {', '.join(missing_columns)}"
            return jsonify({"error": error_msg}), 400

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if all(cell is not None and cell != '' for cell in row):
                params = [
                    session['login_user']['user_id'],
                    row[header.index('ChannelKindName')],
                    row[header.index('AgencyCode')],
                    row[header.index('ContactStyle')],
                    row[header.index('SupportKind')],
                    row[header.index('SupportQty')],
                    row[header.index('SupportAmt')],
                    row[header.index('ChannelPromoID')],
                    row[header.index('ContactDate')],
                    row[header.index('CompleteDate')],
                    row[header.index('Title')],
                    row[header.index('Contents')]
                ]

                try:
                    conn.execute_without_return(
                        "uspSetChannelSupportExcelInsert @ChannelUserID=?, @ChannelKindName=? "
                        ", @AgencyCode=?, @ContactStyle=?, @SupportKind=?, @SupportQty=?, @SupportAmt=? "
                        ", @ChannelPromoID=?, @ContactDate=?, @CompleteDate=?"
                        ", @Title=?, @Contents=?", 
                        params
                    )
                except Exception as e:
                    return jsonify({"error": str(e)}), 400

    return jsonify({"result": "success"})

@bp.route('/get_counsel_content', methods=['GET'])
@login_required
def get_counsel_content():
    channel_manage_id = request.args.get('channel_manage_id')
    
    try:
        res = conn.execute_return('uspGetChannelManageContent @ChannelManageID=?', channel_manage_id)
        
        if res:
            return jsonify({'content': res.Contents}), 200
        else:
            return jsonify({'error': '공지를 찾을 수 없습니다.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500   

