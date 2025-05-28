import re
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

SERVICE_NAMES = {
    1: "베이비리그",
    2: "주니어/튜터링",
    61: "주니어플러스",
}

ROUTE_KINDS = {
    1: {"name": "영상", "icon": "movie"},
    2: {"name": "음원", "icon": "music_note"},
    3: {"name": "첨부파일", "icon": "inventory"},
    4: {"name": "슬라이드", "icon": "photo"},
    5: {"name": "영상모음", "icon": "video_library"},
    6: {"name": "음원모음", "icon": "headphones"},
    7: {"name": "교육", "icon": "school"},
}

PRODUCT_NAMES = {
    0: "공통",
    3: "베이비리그",
    4: "튼튼영어 주니어",
    5: "튼튼영어 튜터링",
    62: "튼튼영어 주니어플러스",
    121: "주니어플러스 규리앤패밀리",
    63: "주니어플러스 LEVEL1",
    64: "주니어플러스 LEVEL2",
    65: "주니어플러스 LEVEL3",
    91: "주니어플러스 MORE",
    103: "스페셜 클래스",
    120: ""  # 공통 메뉴는 이름이 보이지 않아야 함
}

PRODUCT_COMMENTS = {
    3: "PLAY! LEARN! GROW! <br /> 하루종일 신나는 영어놀이터",
    4: "집에서 만나는 영어유치원 <br />우리집에서 나만의 선생님과 1:1로!",
    5: "결과가 다른 초등영어",
    103: "정규 프로그램에 시너지를 더해주는",
    120: ""  # 공통 메뉴는 이름이 보이지 않아야 함
}

BOARD_NAMES = {
    104: "공지사항",
    105: "자료실",
    106: "체험관리",
    107: "상담관리",
    110: "맘스 클래스",
    111: "특별교육",
    112: "특강 자료실",
    114: "교육컨설팅/상담"
}

BOOKLET_KIND_NAMES = {
    117: "스토리북",
    118: "연상력 그림장",
    119: "부가자료",
}

LOGO_IMAGES = {
    3: "/static/images/logo/brand_logo_bl.png",
    4: "/static/images/logo/brand_logo_jr.png",
    5: "/static/images/logo/brand_logo_tr.png",
    62: "/static/images/logo/jp_logo.png",
    63: "/static/images/logo/jp_level1_1.png",
    64: "/static/images/logo/jp_level2_1.png",
    65: "/static/images/logo/jp_level3_1.png",
    91: "/static/images/logo/jp_more.png",
    121: "/static/images/logo/jp_level0.png",
}

BACKGROUND_IMAGES = {
    'main_list': {
        3: "/static/images/main/main_berry.png",
        4: "/static/images/main/main_junior.png",
        5: "/static/images/main/main_tutoring.png",
        62: "/static/images/main/main_jrp.png",
        63: "/static/images/main/jp_level1_1.png",
        64: "/static/images/main/jp_level2_1.png",
        65: "/static/images/main/jp_level3_1.png",
        91: "/static/images/main/jp_more.png",
        103: "/static/images/main/main_anyone.png"
    },
    'title_list': {
        3: "/static/images/main/main_berry.png",
        4: "/static/images/main/main_junior.png",
        5: "/static/images/main/main_tutoring.png",
        62: "/static/images/main/main_jrp.png",
        63: "/static/images/main/jp_level1_1.png",
        64: "/static/images/main/jp_level2_1.png",
        65: "/static/images/main/jp_level3_1.png",
        91: "/static/images/main/jp_more.png",
        98: "/static/images/main/jp_more_level1.png",
        99: "/static/images/main/jp_more_level2.png",
        101: "/static/images/main/jp_more_level3.png",
        103: "/static/images/main/bg_anyone.png",
        121: "/static/images/main/jp_level0.png",
    },
    'content_list': {
        3: "/static/images/main/bg_berry.png",
        4: "/static/images/main/bg_junior.png",
        5: "/static/images/main/bg_tutoring.png",
        62: "/static/images/main/main_jrp.png",
        63: "/static/images/main/jp_level1_1.png",
        64: "/static/images/main/jp_level2_1.png",
        65: "/static/images/main/jp_level3_1.png",
        91: "/static/images/main/jp_more.png",
        98: "/static/images/main/jp_more_level1.png",
        99: "/static/images/main/jp_more_level2.png",
        101: "/static/images/main/jp_more_level3.png",
        103: "/static/images/main/bg_anyone.png",
        121: "/static/images/main/jp_level0.png",
    },
    'board_list': {
        3: "/static/images/main/main_berry.png",
        4: "/static/images/main/main_junior.png",
        5: "/static/images/main/main_tutoring.png",
        62: "/static/images/main/main_jrp.png",
        103: "/static/images/main/main_anyone.png",
    }
}


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


def new_image_url(url):
    new_url = url.replace("/assets/img", "/static/images")
    return new_url


def route_kind_info(route_kind_id, info_type):
    default_service_types = {"name": "Unknown", "icon": "share"}
    route_kind = ROUTE_KINDS.get(route_kind_id, default_service_types)
    return route_kind.get(info_type)


def service_kind_name(service_kind_id):
    return SERVICE_NAMES.get(service_kind_id, "")


def product_kind_name(product_kind_id):
    return PRODUCT_NAMES.get(product_kind_id, "")


def board_kind_name(board_kind_id):
    return BOARD_NAMES.get(board_kind_id, "")


def booklet_kind_name(booklet_kind_id):
    return BOOKLET_KIND_NAMES.get(booklet_kind_id, "")


def background_url(product_kind_id, location='main_list'):
    default_image = "/static/images/main/bg_class.png"
    return BACKGROUND_IMAGES.get(location, {}).get(product_kind_id, default_image)


def logo_url(product_kind_id):
    default_image = ""
    return LOGO_IMAGES.get(product_kind_id, default_image)


def product_comment(product_kind_id):
    default_comment = ""
    return PRODUCT_COMMENTS.get(product_kind_id, default_comment)


def highlight_search(text, search_keyword):
    if not search_keyword or search_keyword == "":
        return text

    regex = re.compile(re.escape(search_keyword), re.IGNORECASE)
    highlighted_text = regex.sub(lambda match: f'<span style="background-color: yellow;">{match.group()}</span>', text)

    return highlighted_text


def virtual_path(path):
    new_path = path.replace(current_app.config['UPLOAD_FOLDER'], "/virtual_path").replace("\\", "/")
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