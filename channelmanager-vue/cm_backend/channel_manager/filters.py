import random
from flask import current_app
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

# basic filter
# safe: html tag 반영
# striptags: html tag를 벗겨냄
# abs: 절대값
# filesizeformat: 파일사이즈 표기, (True) 인자값을 넣으면 바이너리 파일사이즈로 표기
# replace: 교체
# trim: 공백 제거
# int, float, round
# center(중앙위치), wordwrap(줄바꿈), truncate(...)

# template filter
# {{ today | ymd('%m-%d') }}
# {{ today | ymd('%m-%d') | safe }} html tag를 함께 반영하려면.
# {{ today | ymd('%m-%d') | safe | striptags }} html tag를 다시 해제하려면.
# {{ title | truncate(10) }} 10글자로 제한하려면.

CHANNEL_KINDS = {
    1: {"name": "방문사업", "color": "bg-primary", "background": "tuntun.jpg"},
    2: {"name": "베이비리그", "color": "bg-danger", "background": "babyleague.jpg"},
    3: {"name": "마스터클럽", "color": "bg-info", "background": "masterclub.jpg"},
    4: {"name": "프리스쿨", "color": "bg-success", "background": "preschool.jpg"},
    5: {"name": "라트주니어", "color": "bg-warning", "background": "lattjr.jpg"},
    77: {"name": "주니어플러스", "color": "bg-purple", "background": "juniorplus.jpg"},
}

ENDPOINT_ROUTES = {
    'homes.index': {"title": "메인 페이지", "name": "Dashboards"},
    'homes.notice_list': {"title": "공지사항", "name": "Dashboards"},
    'homes.version_history': {"title": "개발이력 안내", "name": "What's New"},
    'admins.user_list': {"title": "사용자 관리", "name": "Admins"},
    'admins.notice_list': {"title": "공지사항 관리", "name": "Admins"},
    'admins.report_list': {"title": "비즈니스 리포트", "name": "EmailReports"},
    'admins.report_modify': {"title": "비즈니스 리포트", "name": "EmailReports"},
    'admins.notice_modify': {"title": "공지사항 관리", "name": "Admins"},
    'accounts.user_update': {"title": "사용자정보 변경", "name": "Users"},
    'counsels.agency_list': {"title": "파트너", "name": "Dashboards"},
    'counsels.agency_map': {"title": "파트너 위치", "name": "Dashboards"},
    'counsels.counsel_agency_list': {"title": "파트너 목록", "name": "Counsels"},
    'counsels.agency_consult_list': {"title": "파트너 상담", "name": "Counsels"},
    'counsels.agency_support_list': {"title": "파트너 지원", "name": "Counsels"},
    'counsels.agency_violation_list': {"title": "파트너 위반", "name": "Counsels"},
    'counsels.consult_list': {"title": "상담", "name": "Counsels"},
    'counsels.consult_modify': {"title": "상담", "name": "Counsels"},
    'counsels.consult_total_list': {"title":"전체채널 상담", "name": "Counsels"},
    'counsels.support_list': {"title": "지원", "name": "Counsels"},
    'counsels.support_modify': {"title": "지원", "name": "Counsels"},
    'counsels.support_total_list': {"title": "전체채널 지원", "name": "Counsels"},
    'counsels.violation_list': {"title": "위반", "name": "Counsels"},
    'counsels.violation_modify': {"title": "위반", "name": "Counsels"},
    'counsels.violation_total_list': {"title": "전체채널 위반", "name": "Counsels"},
    'sources.experience_list': {"title": "체험신청 소스", "name": "Sources"},
    'sources.moms_class_list': {"title": "맘스클래스 소스", "name": "Sources"},
    'sources.internal_list': {"title": "자체 소스", "name": "Sources"},
    'sources.event_list': {"title": "이벤트 소스", "name": "Sources"},
    'sources.level_test_list': {"title": "레벨테스트 소스", "name": "Sources"},
    'sources.reward_list': {"title": "리워드 소스", "name": "Sources"},
    'manages.promo_list': {"title": "프로모션", "name": "Manages"},
    'manages.promo_modify': {"title": "프로모션", "name": "Manages"},
    'manages.goal_list': {"title": "목표관리", "name": "Manages"},
    'manages.goal_modify': {"title": "목표관리", "name": "Manages"},
}

def init_app(app):
    """필터를 애플리케이션에 등록"""
    app.template_filter('datetime_str')(datetime_str)
    app.template_filter('new_image_url')(new_image_url)
    app.template_filter('virtual_path')(virtual_path)
    app.template_filter('image_file_yn')(image_file_yn)
    app.template_filter('channel_background')(channel_background)
    app.template_filter('channel_color')(channel_color)
    app.template_filter('channel_name')(channel_name)
    app.template_filter('endpoint_info')(endpoint_info)
    app.template_filter('sub_background_url')(sub_background_url)
    app.template_filter('number_format')(number_format)


def new_image_url(url):
    new_url = url.replace("/assets/img", "/static/images")
    return new_url


def virtual_path(path):
    new_path = path.replace(current_app.config['UPLOAD_FOLDER'], "/virtual_path").replace("\\", "/")
    # new_path = path.replace("/DailyTuntun", "/virtual_path")
    return new_path


def image_file_yn(file_path):
    image_file_format = ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"]

    r_idx = file_path.rindex('.')
    if r_idx == -1:
        res = False
    else:
        file_format = file_path[r_idx+1:]
        res = True if file_format in image_file_format else False
    return res


def channel_background(channel_id):
    return CHANNEL_KINDS.get(channel_id, {"background": "tuntun.jpg"})["background"]


def channel_color(channel_id):
    return CHANNEL_KINDS.get(channel_id, {"color": "bg-primary"})["color"]


def channel_name(channel_id):
    return CHANNEL_KINDS.get(channel_id, {"name": "방문사업"})["name"]


def endpoint_info(endpoint, type):
    val = "미정"
    if type == 'title':
        val = ENDPOINT_ROUTES.get(endpoint, {"title": "미정"})["title"]
    elif type == 'name':
        val = ENDPOINT_ROUTES.get(endpoint, {"name": "미정"})["name"]
    return val


def sub_background_url(content_group_id):
    background_path = "/static/images/sub/GSH_bg.png"

    if content_group_id == 2:
        background_path = "/static/images/sub/EB_Level1_bg.png"
    elif content_group_id == 3:
        background_path = "/static/images/sub/EB_Level2_bg.png"
    elif content_group_id == 4:
        background_path = "/static/images/sub/EB_Level3_bg.png"
    elif content_group_id == 8:
        background_path = "/static/images/sub/LtR1_bg.png"
    elif content_group_id == 9:
        background_path = "/static/images/sub/LtR2_bg.png"
    elif content_group_id == 10:
        background_path = "/static/images/sub/LtR3_bg.png"

    return background_path


def datetime_str(dt, fmt='date'):
    if isinstance(dt, date):
        if fmt=='time': 
            return "%s" % dt.strftime('%H:%M')
        elif fmt=='month':
            return dt.strftime('%Y-%m')
        else:  
            if dt.date() == date.today():
                return "%s" % dt.strftime('%H:%M')
            else:
                return "%s" % dt.strftime('%Y-%m-%d')
    else:
        return dt


def number_format(value):
    try:
        num = float(value)
        if num.is_integer():
            return "{:,}".format(int(num))
        return "{:,}".format(num)
    except (ValueError, TypeError):
        return value