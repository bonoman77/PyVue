import channel_manager.dbconns as conn
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from channel_manager.utils.auth_handler import login_required
from flask import Blueprint, current_app, request, session, render_template, redirect, url_for, flash, jsonify
from channel_manager.utils.mail_handler import send_report_mail
from channel_manager.enums import ChannelKind, ReportKind

bp = Blueprint('emails', __name__)

def get_business_reports(report_date):
    """여러 종류의 사업자료를 가져오는 함수"""
    try:
        # 사업본부 매출 보고서
        tuntun_sales_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.TUNTUN.value, report_date])
        # 누적데이터 활용: uspBatchChannelReportTuntunSalesDailyStack
        tuntun_sales = {
            'title': tuntun_sales_info.Title,
            'recipients': tuntun_sales_info.Recipients,
            'report_date': tuntun_sales_info.ReportDate,
            'product_sales': conn.return_list('uspGetChannelReportTuntunProductSales @SetDate=?', report_date),
            'product_detail_sales': conn.return_list('uspGetChannelReportTuntunProductDetailSales @SetDate=?', report_date),
            'product_region_sales': conn.return_list('uspGetChannelReportTuntunProductRegionSales @SetDate=?', report_date), 
            'channel_consult': conn.return_list('uspGetChannelReportChannelConsult @ChannelKindID=?, @SetDate=?', [ChannelKind.TUNTUN.value, report_date]), 
            'customer_consult': conn.return_list('uspGetChannelReportCustomerConsult @ChannelKindID=?, @SetDate=?', [ChannelKind.TUNTUN.value, report_date]), 
        }

        masterclub_sales_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.MASTERCLUB.value, report_date])

        # 마스터클럽 매출 보고서 (CS 문의 포함)
        masterclub_sales = {
            'title': masterclub_sales_info.Title,
            'recipients': masterclub_sales_info.Recipients,
            'report_date': masterclub_sales_info.ReportDate,
            'product_region_sales': conn.return_list('uspGetChannelReportMasterclubProductRegionSales @SetDate=?', report_date), 
            'channel_consult': conn.return_list('uspGetChannelReportChannelConsult @ChannelKindID=?, @SetDate=?', [ChannelKind.MASTERCLUB.value, report_date]), 
            'customer_consult': conn.return_list('uspGetChannelReportCustomerConsult @ChannelKindID=?, @SetDate=?', [ChannelKind.MASTERCLUB.value, report_date]), 
        }

        masterclub_orders_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.MASTERCLUB_ORDER.value, report_date])

        # 마스터클럽 사업 보고서 (CS 문의 포함)
        masterclub_orders = {
            'title': masterclub_orders_info.Title,
            'recipients': masterclub_orders_info.Recipients,
            'report_date': masterclub_orders_info.ReportDate,
            'sales': conn.return_list('uspGetChannelReportMasterclubSales @SetDate=?', report_date), 
            'contrast_sales': conn.return_list('uspGetChannelReportMasterclubContrastSales @SetDate=?', report_date), 
        }

        group_sales_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.GROUP.value, report_date])

        # 단체사업 매출 보고서 (CS 문의 포함)
        group_sales = {
            'title': group_sales_info.Title,
            'recipients': group_sales_info.Recipients,
            'report_date': group_sales_info.ReportDate,
            'product_sales': conn.return_list('uspGetChannelReportGroupProductSales @SetDate=?', report_date), 
            'channel_consult': conn.return_list('uspGetChannelReportChannelConsult @ChannelKindID=?, @SetDate=?', [ChannelKind.PRESCHOOL.value, report_date]), 
            'customer_consult': conn.return_list('uspGetChannelReportCustomerConsult @ChannelKindID=?, @SetDate=?', [ChannelKind.PRESCHOOL.value, report_date]), 
        }

        preschool_sales_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.PRESCHOOL.value, report_date])

        # 프리스쿨 매출 보고서
        preschool_sales = {
            'title': preschool_sales_info.Title,
            'recipients': preschool_sales_info.Recipients,
            'report_date': preschool_sales_info.ReportDate,
            'report_range': preschool_sales_info.ReportRange,
            'product_sales': conn.return_list('uspGetChannelReportPreschoolProductSales'), 
        }

        lattjr_sales_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.LATTJR.value, report_date])

        # 라트주니어 매출 보고서
        lattjr_sales = {
            'title': lattjr_sales_info.Title,
            'recipients': lattjr_sales_info.Recipients,
            'report_date': lattjr_sales_info.ReportDate,
            'report_range': lattjr_sales_info.ReportRange,
            'product_sales': conn.return_list('uspGetChannelReportLattjrProductSales'), 
        }

        # 온라인 소스 수집 보고서
        online_sources_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.SOURCE.value, report_date])

        online_sources = {
            'title': online_sources_info.Title,
            'recipients': online_sources_info.Recipients,
            'report_date': online_sources_info.ReportDate,
            'main_stats': conn.return_list('uspGetChannelReportSourceMainList'), 
            'sub_stats': conn.return_list('uspGetChannelReportSourceSubList'),
        }

        health_report_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.HEALTH.value, report_date])

        # SQL 서버 상태 리포트
        health_report = conn.return_list('uspGetSQLServerHealthReport')
        sql_server_health = {
            'title': health_report_info.Title,
            'recipients': health_report_info.Recipients,
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'system_info': [item for item in health_report if item.CategoryName == '시스템 정보'],
            'performance_metrics': [item for item in health_report if item.CategoryName == '성능 지표'],
            'database_info': [item for item in health_report if item.CategoryName == '데이터베이스 정보'],
            'connection_info': [item for item in health_report if item.CategoryName == '연결 정보'],
            'query_performance': [item for item in health_report if item.CategoryName == '쿼리 성능'],
            'blocking_info': [item for item in health_report if item.CategoryName == '차단 정보'],
            'backup_info': [item for item in health_report if item.CategoryName == '백업 정보'],
            'index_info': [item for item in health_report if item.CategoryName == '인덱스 정보'],
            'disk_info': [item for item in health_report if item.CategoryName == '디스크 정보'],
            'target_databases': ['AgencyBiz', 'BabyLeague', 'CorpBiz', 'CorpWorkBiz', 'JuniorPlus', 'LattJr', 'Kunbaeum', 'MemberBiz', 'MasterClub'],
        }

        schedule_report_info = conn.execute_return('uspGetChannelReportMainInfo @ReportKindID=?, @SetDate=?', [ReportKind.SCHEDULE.value, report_date])

        # SQL 서버 스케줄 실패 리포트
        sql_server_schedule = {
            'title': schedule_report_info.Title,
            'recipients': schedule_report_info.Recipients,
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'schedule_list': conn.return_list('uspGetSQLServerScheduleReport'),
        }

        return {
            'tuntun_sales': tuntun_sales,
            'masterclub_sales': masterclub_sales,
            'masterclub_orders': masterclub_orders,
            'group_sales': group_sales,
            'preschool_sales': preschool_sales,
            'lattjr_sales': lattjr_sales,
            'online_sources': online_sources,
            'sql_server_health': sql_server_health,
            'sql_server_schedule': sql_server_schedule,
        }

    except Exception as e:
        current_app.logger.error(f"Failed to get business reports: {str(e)}")
        return {}

def format_report_content(report_kind, data):
    """보고서 데이터를 HTML 형식으로 변환"""
    try:
        if report_kind == 'tuntun_sales':
            return render_template('emails/reports/tuntun_sales_report.html', data=data)
        elif report_kind == 'masterclub_sales':
            return render_template('emails/reports/masterclub_sales_report.html', data=data)
        elif report_kind == 'masterclub_orders':
            return render_template('emails/reports/masterclub_orders_report.html', data=data)
        elif report_kind == 'group_sales':
            return render_template('emails/reports/group_sales_report.html', data=data)
        elif report_kind == 'lattjr_sales':
            return render_template('emails/reports/lattjr_sales_report.html', data=data)
        elif report_kind == 'preschool_sales':
            return render_template('emails/reports/preschool_sales_report.html', data=data)
        elif report_kind == 'online_sources':
            return render_template('emails/reports/online_sources_report.html', data=data)
        elif report_kind == 'sql_server_health':
            return render_template('emails/reports/sql_server_health_report.html', data=data)
        elif report_kind == 'sql_server_schedule':
            return render_template('emails/reports/sql_server_schedule_report.html', data=data)
    except Exception as e:
        current_app.logger.error(f"Failed to format report content: {str(e)}")
        return ""

def send_automated_email(time_group='morning'):
    """자동화된 이메일 발송 함수"""

    try:
        now = datetime.now()    
        report_date = date.today() - timedelta(days=1) if now.hour < 9 else date.today()
        report_date = report_date.strftime('%Y-%m-%d')

        if time_group != 'daily':
            # 타임그룹이 daily가 아닌 경우 휴일 확인 
            is_holiday = conn.execute_return('uspGetChannelHolidayCheckYn @ReportDate=?', report_date)
            
            if is_holiday:
                return

        # 수신자 목록 가져오기
        recipients = conn.return_list('uspGetChannelEmailRecipients')
        # 각 수신자의 구독 정보 가져오기
        subscriptions = conn.return_list('uspGetChannelEmailSubscriptions')
        # 보고서 데이터 가져오기
        reports = get_business_reports(report_date)
        
        if time_group == 'morning':
            report_kinds = ['tuntun_sales', 'masterclub_sales', 'group_sales', 'lattjr_sales', 'preschool_sales', 'sql_server_health']
        elif time_group == 'daily':
            report_kinds = ['online_sources', 'sql_server_schedule']
        elif time_group == 'masterclub_order_after':
            report_kinds = ['masterclub_orders']
        elif time_group == 'tuntun_order_after':
            report_kinds = ['tuntun_sales']

        for recipient in recipients:
            # 수신자별 구독 정보 필터링
            user_subs = [sub for sub in subscriptions if sub.ChannelUserID == recipient.ChannelUserID]
          
            if not user_subs:
                continue
                
            # 구독한 보고서만 발송
            for sub in user_subs:
                report_kind = sub.ReportKind
                # 현재 시간대에 발송해야 하는 보고서인지 확인
                if report_kind not in report_kinds:
                    continue

                if report_kind in reports:  # 보고서 데이터가 있는 경우만
                    report_data = reports[report_kind]

                    # 보고서 데이터가 None인 경우 건너뛰기 (sql_server_schedule 등의 경우)
                    if report_data is None:
                        current_app.logger.info(f"보고서 데이터 없음: {report_kind}")
                        continue

                    if report_kind == 'sql_server_schedule' and (not report_data.get('schedule_list') or len(report_data.get('schedule_list', [])) == 0):
                        current_app.logger.info(f"보고서 데이터 비어 있음: {report_kind} (schedule_list 없음)")
                        continue


                    # 보고서 HTML 생성
                    html_content = format_report_content(report_kind, report_data)
                
                    if html_content:  # HTML 생성이 성공한 경우만
                        params = [recipient.ChannelUserID, time_group, report_kind, datetime.now().strftime('%Y-%m-%d')]
                        is_send = conn.execute_return('uspGetChannelEmailSendLog @ChannelUserID=?, @TimeGroup=?, @ReportKind=?, @SendDate=?', params)

                        if is_send:
                            continue                        

                        if send_report_mail(
                            recipient_email=recipient.UserEmail,
                            subject=f"{sub.Title} {report_date}",
                            html_content=html_content
                        ):  
                            current_app.logger.info(f"성공: {report_date} {recipient.ChannelUserID} {report_kind} {time_group} {recipient.UserEmail}")
                            conn.execute_without_return('uspSetChannelEmailSendLog @ChannelUserID=?, @TimeGroup=?, @ReportKind=?, @SendDate=?', params)
                    else:
                        current_app.logger.error(f"HTML 생성 실패: {report_kind}")

    except Exception as e:
        current_app.logger.error(f"Failed to send automated emails: {str(e)}")


@bp.route("/test", methods=['GET'])
@login_required
def send_test_email():
    try:
        send_automated_email()
        flash("테스트 이메일이 발송되었습니다.", category="success")
    except Exception as e:
        flash(f"이메일 발송 실패: {str(e)}", category="error")
    return redirect(url_for('admins.report_list', channel_id=1))


