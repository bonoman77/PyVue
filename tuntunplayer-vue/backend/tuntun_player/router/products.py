import os
import tuntun_player.dbconns as conn
from flask import Blueprint, current_app, request, session, render_template, redirect, flash, url_for, jsonify
from tuntun_player.enums import BookletKind, RouteKind, ProductKind, ContentGroup
from tuntun_player.utils.page_handler import paged_list
from tuntun_player.utils.auth_handler import login_required, admin_required
from tuntun_player.utils.file_handler import FileHandler

bp = Blueprint('products', __name__)

@bp.route("/main_group_list/<int:product_kind_id>", methods=['GET'])
def main_group_list(product_kind_id):
    res_list = conn.return_list('uspGetStreamContentMainGroupList @ProductKindID=?', product_kind_id)
    return render_template('products/main_group_list.html', res_list=res_list, product_kind_id=product_kind_id)


@bp.route("/main_list/<int:product_kind_id>/<int:product_kind_sub_id>", methods=['GET'])
def main_list(product_kind_id, product_kind_sub_id):
    login_user = session.get('login_user', None)
    manager_yn = login_user.get('manager_yn', 0) if login_user else 0

    sub_name = ""

    if product_kind_sub_id == 0:
        proc = 'uspGetStreamContentMainList @ProductKindID=?, @ManagerYn=?'
        res_list = conn.return_list(proc, [product_kind_id, manager_yn])
    else:
        proc_sub = 'uspGetStreamContentProductKindSubName @ProductKindSubID=?'
        sub_name = conn.execute_return(proc_sub, product_kind_sub_id).Item

        proc = 'uspGetStreamContentMainSubList @ProductKindID=?, @ProductKindSubID=?, @ManagerYn=?'
        params = [product_kind_id, product_kind_sub_id, manager_yn]
        res_list = conn.return_list(proc, params)

    return render_template('products/main_list.html', res_list=res_list
                           , sub_name=sub_name, product_kind_id=product_kind_id
                           , ProductKind=ProductKind)


@bp.route("/title_search_list/<int:product_kind_id>", methods=['GET'])
@login_required
def title_search_list(product_kind_id):
    search_text = request.args.get('search_text')
    print(search_text)
    member_id = session['login_user']['member_id']
    manager_yn = session['login_user']['manager_yn']

    if product_kind_id == ProductKind.BABY_LEAGUE.value:
        proc = "uspGetStreamContentTitleSearchListBerry @MemberID=?, @ProductKindID=?, @SearchText=?"
    elif product_kind_id in [ProductKind.JUNIOR.value, ProductKind.TUTORING.value]:
        proc = "uspGetStreamContentTitleSearchList @MemberID=?, @ProductKindID=?, @SearchText=?"
    else:
        proc = "uspGetStreamContentTitleSearchListPlus @MemberID=?, @ProductKindID=?, @SearchText=?"

    if manager_yn:
        proc = "uspGetStreamContentTitleSearchListManager @MemberID=?, @ProductKindID=?, @SearchText=?"

    params = [member_id, product_kind_id, search_text]
    res_list = conn.return_list(proc, params)

    return render_template('products/title_search_list.html', product_kind_id=product_kind_id
                           , res_list=res_list, search_text=search_text)


@bp.route("/title_list/<int:product_kind_id>/<int:content_group_id>", methods=['GET'])
@login_required
def title_list(product_kind_id, content_group_id):
    member_id = session['login_user']['member_id']
    manager_yn = session['login_user']['manager_yn']

    if manager_yn and content_group_id in [ContentGroup.SING.value, ContentGroup.DANCE.value]:
        manager_content = ContentGroup.SING_DANCE.value
        return redirect(url_for('products.title_list', product_kind_id=product_kind_id, content_group_id=manager_content))

    if manager_yn and product_kind_id in [ProductKind.JUNIOR_PLUS_LEVEL1.value, ProductKind.JUNIOR_PLUS_LEVEL2.value, ProductKind.JUNIOR_PLUS_LEVEL3.value]:
        if content_group_id in [cg.value for cg in ContentGroup if cg.name.startswith('PLUS_')]:
            return redirect(url_for('products.main_list', product_kind_id=product_kind_id, product_kind_sub_id=0))

    res = conn.execute_return('uspGetStreamContentGroupInfo @ContentGroupID=?', content_group_id)

    if product_kind_id == ProductKind.BABY_LEAGUE.value:
        proc_upper = "uspGetStreamContentUpperListBerry @MemberID=?, @ContentGroupID=?"
        proc_list = "uspGetStreamContentTitleListBerry @MemberID=?, @ContentGroupID=?"
    elif product_kind_id in [ProductKind.JUNIOR.value, ProductKind.TUTORING.value]:
        proc_upper = "uspGetStreamContentUpperList @MemberID=?, @ContentGroupID=?"
        proc_list = "uspGetStreamContentTitleList @MemberID=?, @ContentGroupID=?"
    else:
        proc_upper = "uspGetStreamContentUpperListPlus @MemberID=?, @ContentGroupID=?"
        proc_list = "uspGetStreamContentTitleListPlus @MemberID=?, @ContentGroupID=?"

    if manager_yn:
        proc_upper = "uspGetStreamContentUpperListManager @MemberID=?, @ContentGroupID=?"
        proc_list = "uspGetStreamContentTitleListManager @MemberID=?, @ContentGroupID=?"

    upper_list = conn.return_list(proc_upper, [member_id, content_group_id])
    res_list = conn.return_list(proc_list, [member_id, content_group_id])

    return render_template('products/title_list.html', res=res, upper_list=upper_list, res_list=res_list)


@bp.route("/content_list/<int:product_kind_id>/<int:content_title_id>", methods=['GET'])
@login_required
def content_list(product_kind_id, content_title_id):
    member_id = session['login_user']['member_id']
    manager_yn = session['login_user']['manager_yn']

    proc_reference = "uspGetStreamContentReferenceMainList @ContentTitleID=?"
    file_list = conn.return_list(proc_reference, content_title_id) if manager_yn else ""

    if product_kind_id == ProductKind.BABY_LEAGUE.value:
        proc = "uspGetStreamContentTitleDetailBerry @MemberID=?, @ContentTitleID=?"
        proc_list = "uspGetStreamContentListBerry @MemberID=?, @ContentTitleID=?"
        proc_music_list = "uspGetStreamContentMusicListBerry @MemberID=?, @ContentTitleID=?"
    elif product_kind_id in [ProductKind.JUNIOR.value, ProductKind.TUTORING.value]:
        proc = "uspGetStreamContentTitleDetail @MemberID=?, @ContentTitleID=?"
        proc_list = "uspGetStreamContentList @MemberID=?, @ContentTitleID=?"
        proc_music_list = "uspGetStreamContentList @MemberID=?, @ContentTitleID=?"
    else:
        proc = "uspGetStreamContentTitleDetailPlus @MemberID=?, @ContentTitleID=?"
        proc_list = "uspGetStreamContentListPlus @MemberID=?, @ContentTitleID=?"
        proc_music_list = "uspGetStreamContentMusicListPlus @MemberID=?, @ContentTitleID=?"

    if manager_yn:
        proc = "uspGetStreamContentTitleDetailManager @MemberID=?, @ContentTitleID=?"
        proc_list = "uspGetStreamContentListManager @MemberID=?, @ContentTitleID=?"
        proc_music_list = "uspGetStreamContentMusicListManager @MemberID=?, @ContentTitleID=?"

    res = conn.execute_return(proc, [member_id, content_title_id])
    res_list = conn.return_list(proc_list, [member_id, content_title_id])
    music_list = conn.return_list(proc_music_list, [member_id, content_title_id])

    return render_template('products/content_list.html', res=res, file_list=file_list
                           , res_list=res_list, music_list=music_list, product_kind_id=product_kind_id)


@bp.route("/content_view", methods=['GET'])
@login_required
def content_view():
    member_id = session['login_user']['member_id']
    stream_id = request.args.get('stream_id')
    proc = "uspSetStreamMemberContentView @MemberID=?, @StreamID=?"
    conn.execute_without_return(proc, [member_id, stream_id])

    return jsonify({"result": "success"})


@bp.route("/content_music_listen", methods=['GET'])
@login_required
def content_music_listen():
    member_id = session['login_user']['member_id']
    content_music_id = request.args.get('content_music_id')
    proc = "uspSetStreamMemberContentMusicListen @MemberID=?, @ContentMusicID=?"
    conn.execute_without_return(proc, [member_id, content_music_id])

    return jsonify({"result": "success"})


@bp.route("/download_list/<int:download_kind_id>", methods=['GET'])
@login_required
def download_list(download_kind_id):
    member_id = session['login_user']['member_id']
    manager_yn = session['login_user']['manager_yn']

    if manager_yn:
        proc = "uspGetStreamDownloadListManager @MemberID=?, @DownloadKindID=?"
    else:
        proc = "uspGetStreamDownloadList @MemberID=?, @DownloadKindID=?"

    params = [member_id, download_kind_id]
    res_list = conn.return_list(proc, params)
    tbuddy_path = r'\\172.16.0.244\naspath\TuntunPlayer\TBuddy'

    return render_template('products/download_list.html',res_list=res_list
                           , download_kind_id=download_kind_id, tbuddy_path=tbuddy_path)


# 즐겨찾기(영상)
@bp.route("/content_favorite_list/<int:product_kind_id>/<int:content_group_id>", methods=['GET'])
@login_required
def content_favorite_list(product_kind_id, content_group_id):
    member_id = session['login_user']['member_id']
    manager_yn = session['login_user']['manager_yn']
    manager_auth_yn = False

    if product_kind_id == ProductKind.BABY_LEAGUE.value:
        proc = "uspGetStreamMyFavoriteContentListBerry @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        proc_tag = "uspGetStreamMyFavoriteContentGroupListBerry @MemberID=?, @ProductKindID=?"
    elif product_kind_id in [ProductKind.JUNIOR.value, ProductKind.TUTORING.value]:
        proc = "uspGetStreamMyFavoriteContentList @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        proc_tag = "uspGetStreamMyFavoriteContentGroupList @MemberID=?, @ProductKindID=?"
    else:
        proc = "uspGetStreamMyFavoriteContentListPlus @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        proc_tag = "uspGetStreamMyFavoriteContentGroupListPlus @MemberID=?, @ProductKindID=?"

    if manager_yn:
        if ProductKind.SPECIAL_CLASS.value:
            manager_auth_yn = True
        else:
            proc_auth = "uspGetStreamMyFavoriteContentManagerAuthYn @MemberID=?, @ProductKindID=?"
            manager_auth_yn = bool(conn.execute_return(proc_auth, [member_id, product_kind_id]).ServiceAuthYn)

        proc = "uspGetStreamMyFavoriteContentListManager @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        proc_tag = "uspGetStreamMyFavoriteContentGroupListManager @MemberID=?, @ProductKindID=?"

    res_list = conn.return_list(proc, [member_id, product_kind_id, content_group_id])
    tag_list = conn.return_list(proc_tag, [member_id, product_kind_id])

    return render_template('products/content_favorite_list.html'
                           , product_kind_id=product_kind_id, content_group_id=content_group_id
                           , res_list=res_list, tag_list=tag_list
                           , manager_auth_yn=manager_auth_yn)


@bp.route("/content_favorite_update", methods=['GET'])
@login_required
def content_favorite_update():
    member_id = session['login_user']['member_id']
    content_id = request.args.get('content_id')
    favorite_yn = request.args.get('favorite_yn')

    proc = 'uspSetStreamContentFavoriteUpdate @MemberID=?, @ContentID=?, @FavoriteYn=?'
    conn.execute_without_return(proc, [member_id, content_id, favorite_yn])

    return jsonify({"result": "success"})


@bp.route("/content_favorite_sort_update", methods=['POST'])
@login_required
def content_favorite_sort_update():
    member_id = session['login_user']['member_id']
    ids = request.json.get('content_ids')
    proc = 'uspSetStreamContentFavoriteSortUpdate @MemberID=?, @ContentID=?, @OrderNum=?'
    for num, i in enumerate(ids):
        conn.execute_without_return(proc, [member_id, i, num])

    return jsonify({"result": "success"})


# 즐겨찾기(음원)
@bp.route("/content_favorite_music_list/<int:product_kind_id>/<int:content_group_id>", methods=['GET'])
@login_required
def content_favorite_music_list(product_kind_id, content_group_id):
    member_id = session['login_user']['member_id']
    manager_yn = session['login_user']['manager_yn']
    manager_auth_yn = False

    if product_kind_id == ProductKind.BABY_LEAGUE.value:
        music = "uspGetStreamMyFavoriteContentMusicListBerry @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        music_tag = "uspGetStreamMyFavoriteContentMusicGroupListBerry @MemberID=?, @ProductKindID=?"

    elif product_kind_id in [ProductKind.JUNIOR.value, ProductKind.TUTORING.value]:
        music = "uspGetStreamMyFavoriteContentMusicList @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        music_tag = "uspGetStreamMyFavoriteContentMusicGroupList @MemberID=?, @ProductKindID=?"
    else:
        music = "uspGetStreamMyFavoriteContentMusicListPlus @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        music_tag = "uspGetStreamMyFavoriteContentMusicGroupListPlus @MemberID=?, @ProductKindID=?"

    if manager_yn:
        if ProductKind.SPECIAL_CLASS.value:
            manager_auth_yn = True
        else:
            proc_auth = "uspGetStreamMyFavoriteContentManagerAuthYn @MemberID=?, @ProductKindID=?"
            manager_auth_yn = bool(conn.execute_return(proc_auth, [member_id, product_kind_id]).ServiceAuthYn)

        music = "uspGetStreamMyFavoriteContentMusicListManager @MemberID=?, @ProductKindID=?, @ContentGroupID=?"
        music_tag = "uspGetStreamMyFavoriteContentMusicGroupListManager @MemberID=?, @ProductKindID=?"

    music_list = conn.return_list(music, [member_id, product_kind_id, content_group_id])
    music_tag_list = conn.return_list(music_tag, [member_id, product_kind_id])

    return render_template('products/content_favorite_music_list.html'
                           , product_kind_id=product_kind_id, content_group_id=content_group_id
                           , music_list=music_list, music_tag_list=music_tag_list
                           , manager_auth_yn=manager_auth_yn)


@bp.route("/content_favorite_music_update", methods=['GET'])
@login_required
def content_favorite_music_update():
    member_id = session['login_user']['member_id']
    content_music_id = request.args.get('content_music_id')
    favorite_yn = request.args.get('favorite_yn')

    proc = 'uspSetStreamContentFavoriteMusicUpdate @MemberID=?, @ContentMusicID=?, @FavoriteYn=?'
    conn.execute_without_return(proc, [member_id, content_music_id, favorite_yn])

    return jsonify({"result": "success"})


@bp.route("/content_favorite_music_sort_update", methods=['POST'])
@login_required
def content_favorite_music_sort_update():
    member_id = session['login_user']['member_id']
    ids = request.json.get('content_music_ids')
    proc = 'uspSetStreamContentFavoriteMusicSortUpdate @MemberID=?, @ContentMusicID=?, @OrderNum=?'
    for num, i in enumerate(ids):
        conn.execute_without_return(proc, [member_id, i, num])

    return jsonify({"result": "success"})


# 연결교재
@bp.route("/admin_product_list/<int:service_kind_id>", methods=['GET'])
@admin_required
def admin_product_list(service_kind_id):
    search_text = '' if request.args.get('search_text') is None else request.args.get('search_text')
    search = {
        'search_text': search_text,
    }

    proc_cnt = 'uspGetStreamAdminServiceProductCnt @ServiceKindID=?, @SearchText=?'
    total = conn.execute_return(proc_cnt, [service_kind_id, search_text]).TotalCnt

    paging_line = 5
    page = int(request.args.get('page', 1))
    row_size = int(request.args.get('row_size', 20))

    paging = paged_list(total, page, paging_line, row_size)

    proc = 'uspGetStreamAdminServiceProductList @ServiceKindID=?, @PageSize=?, @PageNumber=?, @SearchText=?'
    params = [service_kind_id, row_size, page, search_text]
    res_list = conn.return_list(proc, params)

    return render_template('products/admin_product_list.html', service_kind_id=service_kind_id
                           , res_list=res_list, search=search, paging=paging)


@bp.route("/admin_product_code_search", methods=['POST'])
@admin_required
def admin_product_code_search():
    service_kind_id = request.form.get('service_kind_id')
    product_code = request.form.get('product_code')

    proc = 'uspGetStreamSearchProductCode @ServiceKindID=?, @ProductCode=?'

    params = [service_kind_id, product_code]
    res = conn.execute_return(proc, params)

    if not res:
        error_message = "존재하지 않는 교재입니다."
        response_data = {"result": "fail", "message": error_message}
    elif res.ErrorNum == 1:
        error_message = "이미 튼튼플레이어에 등록되어있습니다."
        response_data = {"result": "fail", "message": error_message}
    else:
        response_data = {"result": "success", "product_alias": res.ProductAlias}

    return jsonify(response_data)


@bp.route("/admin_product_insert/<int:service_kind_id>", methods=['GET'])
@admin_required
def admin_product_insert(service_kind_id):

    proc = 'uspGetStreamAdminServiceProductGroupList @ServiceKindID=?'
    params = [service_kind_id]
    res_list = conn.return_list(proc, params)

    return render_template('products/admin_product_insert.html', service_kind_id=service_kind_id
                           , res_list=res_list)


@bp.route("/admin_product_insert", methods=['POST'])
@admin_required
def admin_product_insert_post():
    member_id = session['login_user']['member_id']
    product_code = request.form.get('product_code')
    service_kind_id = request.form.get('service_kind_id')

    proc = 'uspSetStreamAdminServiceProductDelete @ProductCode=?'
    conn.execute_without_return(proc, product_code)

    proc = 'uspSetStreamAdminServiceProductMapping @ProductCode=?, @ContentGroupID=?, @MemberID=?'
    content_group_ids = request.form.getlist('content_group_check')

    for i in content_group_ids:
        params = [product_code, i, member_id]
        conn.execute_without_return(proc, params)

    return redirect(url_for('products.admin_product_list', service_kind_id=service_kind_id))


@bp.route("/admin_product_update/<int:service_kind_id>/<string:product_code>", methods=['GET'])
@admin_required
def admin_product_update(service_kind_id, product_code):
    proc = 'uspGetStreamAdminServiceProductAlias @ServiceKindID=?, @ProductCode=?'
    proc_list = 'uspGetStreamAdminServiceProductGroupMappingList @ServiceKindID=?, @ProductCode=?'

    params = [service_kind_id, product_code]
    product_alias = conn.execute_return(proc, params).ProductAlias
    res_list = conn.return_list(proc_list, params)

    return render_template('products/admin_product_update.html', service_kind_id=service_kind_id
                           , res_list=res_list, product_code=product_code, product_alias=product_alias)


@bp.route("/admin_product_update", methods=['POST'])
@admin_required
def admin_product_update_post():
    member_id = session['login_user']['member_id']

    old_product_code = request.form.get('old_product_code')

    proc = 'uspSetStreamAdminServiceProductDelete @ProductCode=?'
    conn.execute_without_return(proc, old_product_code)

    product_code = request.form.get('product_code')
    service_kind_id = request.form.get('service_kind_id')

    proc = 'uspSetStreamAdminServiceProductMapping @ProductCode=?, @ContentGroupID=?, @MemberID=?'
    content_group_ids = request.form.getlist('content_group_check')

    for i in content_group_ids:
        params = [product_code, i, member_id]
        conn.execute_without_return(proc, params)

    return redirect(url_for('products.admin_product_list', service_kind_id=service_kind_id))


@bp.route("/admin_product_delete", methods=['POST'])
@admin_required
def admin_product_delete_post():
    product_code = request.form.get('product_code')

    proc = 'uspSetStreamAdminServiceProductDelete @ProductCode=?'
    conn.execute_without_return(proc, product_code)

    return jsonify({"result": "success"})


# 컨텐츠 메인그룹 메뉴 (통합 경로, 주니어플러스)
@bp.route("/admin_main_group_list/<int:route_kind_id>/<int:product_kind_id>", methods=['GET'])
@admin_required
def admin_main_group_list(route_kind_id, product_kind_id):
    proc = 'uspGetStreamAdminContentMainGroupList @ProductKindID=?'
    res_list = conn.return_list(proc, product_kind_id)
    return render_template('products/admin_main_group_list.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id)


# 컨텐츠 메인 메뉴 (통합 경로)
@bp.route("/admin_main_list/<int:route_kind_id>/<int:product_kind_id>/<int:manager_yn>", methods=['GET'])
@admin_required
def admin_main_list(route_kind_id, product_kind_id, manager_yn):
    if route_kind_id == RouteKind.REFERENCE.value or route_kind_id == RouteKind.BOOKLET.value:
        manager_yn = True

    if manager_yn:
        proc = 'uspGetStreamAdminContentGroupListManager @ProductKindID=?'
        res_list = conn.return_list(proc, product_kind_id)
    else:
        proc = 'uspGetStreamAdminContentGroupList @ProductKindID=?'
        res_list = conn.return_list(proc, product_kind_id)

    return render_template('products/admin_main_list.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id, manager_yn=manager_yn)


# 컨텐츠 타이틀 메뉴 (통합 경로)
@bp.route("/admin_title_list/<int:route_kind_id>/"
           "<int:product_kind_id>/<int:content_group_id>/<int:manager_yn>", methods=['GET'])
@admin_required
def admin_title_list(route_kind_id, product_kind_id, content_group_id, manager_yn):
    proc = "uspGetStreamAdminContentGroupInfo @ContentGroupID=?"
    content_group = conn.execute_return(proc, content_group_id).ContentGroup
    if manager_yn:
        proc_list = "uspGetStreamAdminContentTitleListManager @ContentGroupID=?"
        res_list = conn.return_list(proc_list, content_group_id)
    else:
        proc_list = "uspGetStreamAdminContentTitleList @ContentGroupID=?"
        res_list = conn.return_list(proc_list, content_group_id)

    return render_template('products/admin_title_list.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id
                           , content_group_id=content_group_id, content_group=content_group, manager_yn=manager_yn)


# 영상 관리
@bp.route("/admin_content_list/<int:route_kind_id>/<int:product_kind_id>/<int:content_title_id>", methods=['GET'])
@admin_required
def admin_content_list(route_kind_id, product_kind_id, content_title_id):
    proc_title = "uspGetStreamAdminContentTitleInfo @ContentTitleID=?"
    content_title = conn.execute_return(proc_title, content_title_id).ContentTitle

    proc = "uspGetStreamAdminContentLinkList @ContentTitleID=?"
    res_list = conn.return_list(proc, content_title_id)

    return render_template('products/admin_content_list.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id
                           , content_title_id=content_title_id, content_title=content_title)


@bp.route("/admin_content_title_insert", methods=['POST'])
@admin_required
def admin_content_title_insert():
    member_id = session['login_user']['member_id']
    content_title_id = request.form.get("content_title_id")
    title = request.form.get("title")

    proc = "uspSetStreamAdminContentTitleInsert @MemberID=?, @ContentTitleID=?, @Title=?"
    params = [member_id, content_title_id, title]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_update", methods=['POST'])
@admin_required
def admin_content_title_update():
    member_id = session['login_user']['member_id']
    content_id = int(request.form.get("content_id"))
    title = request.form.get("title")
    stream_code = request.form.get("stream_code")

    proc = "uspSetStreamAdminContentUpdate @ContentID=?, @MemberID=?, @Title=?, @StreamCode=?"
    params = [content_id, member_id, title, stream_code]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_display_update", methods=['POST'])
@admin_required
def admin_content_display_update():
    content_id = request.form.get('content_id')
    display_yn = request.form.get('display_yn')
    manager_yn = request.form.get('manager_yn')

    proc = 'uspSetStreamAdminContentDisplayYn @ContentID=?, @ManagerYn=?, @DisplayYn=?'
    params = [content_id, manager_yn, display_yn]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_sort_update", methods=['POST'])
@admin_required
def admin_content_sort_update():
    ids = request.json.get('content_ids')
    proc = "uspSetStreamAdminContentSortUpdate @ContentID=?, @OrderNum=?"
    for num, i in enumerate(ids):
        params = [i, num]
        conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_delete", methods=['POST'])
@admin_required
def admin_content_delete():
    content_id = request.form.get('content_id')
    proc = 'uspSetStreamAdminContentDelete @ContentID=?'
    conn.execute_without_return(proc, content_id)

    return jsonify({"result": "success"})


# 음원 관리
@bp.route("/admin_content_music_list"
           "/<int:route_kind_id>/<int:product_kind_id>/<int:content_title_id>", methods=['GET'])
@admin_required
def admin_content_music_list(route_kind_id, product_kind_id, content_title_id):
    proc_title = "uspGetStreamAdminContentTitleInfo @ContentTitleID=?"
    content_title = conn.execute_return(proc_title, content_title_id).ContentTitle

    proc_list = 'uspGetStreamAdminContentMusicList @ContentTitleID=?'
    res_list = conn.return_list(proc_list, content_title_id)

    return render_template('products/admin_content_music_list.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id
                           , content_title_id=content_title_id, content_title=content_title)


@bp.route("/admin_content_music_title_insert", methods=['POST'])
@admin_required
def admin_content_music_title_insert():
    member_id = session['login_user']['member_id']
    content_title_id = int(request.form.get("content_title_id"))
    title = request.form.get("title")

    proc = 'uspSetStreamAdminContentMusicTitleInsert @MemberID=?, @ContentTitleID=?, @Title=?'
    params = [member_id, content_title_id, title]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_music_title_update", methods=['POST'])
@admin_required
def admin_content_music_title_update():
    member_id = session['login_user']['member_id']
    content_music_id = int(request.form.get("content_music_id"))
    title = request.form.get("title")

    proc = "uspSetStreamAdminContentMusicTitleUpdate @ContentMusicID=?, @MemberID=?, @Title=?"
    params = [content_music_id, member_id, title]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_music_display_update", methods=['POST'])
@admin_required
def admin_content_music_display_update():
    content_music_id = request.form.get('content_music_id')
    display_yn = request.form.get('display_yn')
    manager_yn = request.form.get('manager_yn')

    proc = 'uspSetStreamAdminContentMusicDisplayYn @ContentMusicID=?, @ManagerYn=?, @DisplayYn=?'
    conn.execute_without_return(proc, [content_music_id, manager_yn, display_yn])

    return jsonify({"result": "success"})


@bp.route("/admin_content_music_sort_update", methods=['POST'])
@admin_required
def admin_content_music_sort_update():
    ids = request.json.get('content_music_ids')
    proc = 'uspSetStreamAdminContentMusicSortUpdate @ContentMusicID=?, @OrderNum=?'
    for num, i in enumerate(ids):
        conn.execute_without_return(proc, [i, num+1])

    return jsonify({"result": "success"})


@bp.route("/admin_content_music_delete", methods=['POST'])
@admin_required
def admin_content_music_delete():
    content_music_id = request.form.get('content_music_id')
    proc = 'uspSetStreamAdminContentMusicDelete @ContentMusicID=?'
    conn.execute_without_return(proc, content_music_id)

    return jsonify({"result": "success"})


@bp.route("/admin_content_music_file_upload", methods=['POST'])
@admin_required
def admin_content_music_file_upload():
    content_title_id = request.form.get('content_title_id')
    content_music_id = request.form.get('content_music_id')
    member_id = session['login_user']['member_id']

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "ContentMusic", content_title_id)
    upload_files = request.files.getlist('image_file')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamAdminContentMusicFileUpload \
              @ContentMusicID=?, @MemberID=?, @UploadFilePath=?, @UploadFileName=?'
    params = [content_music_id, member_id, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return jsonify({"file_name": file_name_str})


@bp.route("/admin_content_music_file_delete", methods=['POST'])
@admin_required
def admin_content_music_file_delete():
    content_music_id = request.form.get('content_music_id')
    proc = 'uspSetStreamAdminContentMusicFileDelete @ContentMusicID=?'
    conn.execute_without_return(proc, content_music_id)

    return jsonify({"result": "success"})


# 영상모음 관리
@bp.route("/admin_content_upper_list/<int:route_kind_id>/<int:product_kind_id>/<int:content_group_id>", methods=['GET'])
@admin_required
def admin_content_upper_list(route_kind_id, product_kind_id, content_group_id):
    proc_name = "uspGetStreamAdminContentGroupName @ContentGroupID=?"
    group_name = conn.execute_return(proc_name, content_group_id).ContentGroupName

    proc_list = "uspGetStreamAdminContentUpperList @ContentGroupID=?"
    res_list = conn.return_list(proc_list, content_group_id)

    return render_template('products/admin_content_upper_list.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id, content_group_id=content_group_id, group_name=group_name)


@bp.route("/admin_content_upper_title_insert", methods=['POST'])
@admin_required
def admin_content_upper_title_insert():
    member_id = session['login_user']['member_id']
    content_group_id = request.form.get("content_group_id")
    title = request.form.get("title")
    showcase_yn = request.form.get("showcase_yn")

    proc = "uspSetStreamAdminContentUpperTitleInsert @MemberID=?, @ContentGroupID=?, @Title=?, @ShowcaseYn=?"
    params = [member_id, content_group_id, title, showcase_yn]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_update", methods=['POST'])
@admin_required
def admin_content_upper_update():
    member_id = session['login_user']['member_id']
    upper_content_id = int(request.form.get("upper_content_id"))
    title = request.form.get("title")
    stream_code = request.form.get("stream_code")
    showcase_yn = request.form.get("showcase_yn")

    proc = "uspSetStreamAdminContentUpperUpdate @UpperContentID=?, @MemberID=?, @Title=?, @StreamCode=?, @ShowcaseYn=?"
    params = [upper_content_id, member_id, title, stream_code, showcase_yn]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_display_update", methods=['POST'])
@admin_required
def admin_content_upper_display_update():
    upper_content_id = request.form.get('upper_content_id')
    display_yn = request.form.get('display_yn')
    manager_yn = request.form.get('manager_yn')

    proc = 'uspSetStreamAdminContentUpperDisplayYn @UpperContentID=?, @ManagerYn=?, @DisplayYn=?'
    params = [upper_content_id, manager_yn, display_yn]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_sort_update", methods=['POST'])
@admin_required
def admin_content_upper_sort_update():
    ids = request.json.get('upper_content_ids')
    proc = "uspSetStreamAdminContentUpperSortUpdate @UpperContentID=?, @OrderNum=?"
    for num, i in enumerate(ids):
        params = [i, num]
        conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_delete", methods=['POST'])
@admin_required
def admin_content_upper_delete():
    upper_content_id = request.form.get('upper_content_id')
    proc = 'uspSetStreamAdminContentUpperDelete @UpperContentID=?'
    conn.execute_without_return(proc, upper_content_id)

    return jsonify({"result": "success"})


# 음원모음 관리
@bp.route("/admin_content_upper_music_list/<int:route_kind_id>/<int:product_kind_id>/<int:content_group_id>", methods=['GET'])
@admin_required
def admin_content_upper_music_list(route_kind_id, product_kind_id, content_group_id):
    proc_name = "uspGetStreamAdminContentGroupName @ContentGroupID=?"
    group_name = conn.execute_return(proc_name, content_group_id).ContentGroupName

    proc = 'uspGetStreamAdminContentUpperMusicList @ContentGroupID=?'
    res_list = conn.return_list(proc, content_group_id)

    return render_template('products/admin_content_upper_music_list.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id, content_group_id=content_group_id, group_name=group_name)


@bp.route("/admin_content_upper_music_title_insert", methods=['POST'])
@admin_required
def admin_content_upper_music_title_insert():
    member_id = session['login_user']['member_id']
    content_group_id = request.form.get("content_group_id")
    title = request.form.get("title")

    proc = "uspSetStreamAdminContentUpperMusicTitleInsert @MemberID=?, @ContentGroupID=?, @Title=?"
    params = [member_id, content_group_id, title]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_music_title_update", methods=['POST'])
@admin_required
def admin_content_upper_music_title_update():
    member_id = session['login_user']['member_id']
    upper_content_music_id = int(request.form.get("upper_content_music_id"))
    title = request.form.get("title")
    attach_file_yn = request.form.get("attach_file_yn")

    proc = "uspSetStreamAdminContentUpperMusicTitleUpdate @UpperContentMusicID=?, @MemberID=?, @Title=?, @AttachFileYn=?"
    params = [upper_content_music_id, member_id, title, attach_file_yn]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_music_display_update", methods=['POST'])
@admin_required
def admin_content_upper_music_display_update():
    upper_content_music_id = request.form.get('upper_content_music_id')
    display_yn = request.form.get('display_yn')
    manager_yn = request.form.get('manager_yn')

    proc = 'uspSetStreamAdminContentUpperMusicDisplayYn @UpperContentMusicID=?, @ManagerYn=?, @DisplayYn=?'
    params = [upper_content_music_id, manager_yn, display_yn]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_sort_music_update", methods=['POST'])
@admin_required
def admin_content_upper_music_sort_update():
    ids = request.json.get('upper_content_music_id')
    proc = "uspSetStreamAdminContentUpperMusicSortUpdate @UpperContentMusicID=?, @OrderNum=?"
    for num, i in enumerate(ids):
        params = [i, num]
        conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_music_delete", methods=['POST'])
@admin_required
def admin_content_upper_music_delete():
    upper_content_music_id = request.form.get('upper_content_music_id')
    proc = 'uspSetStreamAdminContentUpperMusicDelete @UpperContentMusicID=?'
    conn.execute_without_return(proc, upper_content_music_id)

    return jsonify({"result": "success"})


@bp.route("/admin_content_upper_music_file_upload", methods=['POST'])
@admin_required
def admin_content_upper_music_file_upload():
    upper_content_music_id = request.form.get('upper_content_music_id')
    member_id = session['login_user']['member_id']

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "ContentMusicUpper")
    upload_files = request.files.getlist('image_file')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamAdminContentUpperMusicFileUpload \
              @UpperContentMusicID=?, @MemberID=?, @UploadFilePath=?, @UploadFileName=?'
    params = [upper_content_music_id, member_id, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return jsonify({"file_name": file_name_str})


@bp.route("/admin_content_upper_music_file_delete", methods=['POST'])
@admin_required
def admin_content_upper_music_file_delete():
    upper_content_music_id = request.form.get('upper_content_music_id')
    proc = 'uspSetStreamAdminContentUpperMusicFileDelete @UpperContentMusicID=?'
    conn.execute_without_return(proc, upper_content_music_id)

    return jsonify({"result": "success"})


# 작업중
@bp.route("/admin_content_upper_music_update"
           "/<int:route_kind_id>/<int:product_kind_id>/<int:content_group_id>/<int:upper_content_music_id>"
           , methods=['GET'])
@admin_required
def admin_content_upper_music_update(route_kind_id, product_kind_id, content_group_id, upper_content_music_id):
    proc = "uspGetStreamAdminContentUpperMusicTitle @UpperContentMusicID=?"
    title = conn.execute_return(proc, upper_content_music_id).Title

    proc_list = 'uspGetStreamAdminContentUpperMusicLinkMappingList @ContentGroupID=?, @UpperContentMusicID=?'
    params = [content_group_id, upper_content_music_id]
    res_list = conn.return_list(proc_list, params)

    return render_template('products/admin_content_upper_music_update.html', res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id
                           , content_group_id=content_group_id, title=title
                           , upper_content_music_id=upper_content_music_id)


@bp.route("/admin_content_upper_music_update", methods=['POST'])
@admin_required
def admin_content_upper_music_update_post():

    upper_content_music_id = request.form.get('upper_content_music_id')
    route_kind_id = request.form.get('route_kind_id')
    product_kind_id = request.form.get('product_kind_id')
    content_group_id = request.form.get('content_group_id')

    proc = 'uspSetStreamAdminContentUpperMusicLinkDelete @UpperContentMusicID=?'
    conn.execute_without_return(proc, upper_content_music_id)

    proc = 'uspSetStreamAdminContentUpperMusicLinkMapping @UpperContentMusicID=?, @ContentMusicID=?'
    content_music_ids = request.form.getlist('content_music_check')

    for i in content_music_ids:
        params = [upper_content_music_id, i]
        conn.execute_without_return(proc, params)

    return redirect(url_for('products.admin_content_upper_music_list', route_kind_id=route_kind_id, product_kind_id=product_kind_id, content_group_id=content_group_id))


@bp.route("/admin_content_upper_music_link_delete", methods=['POST'])
@admin_required
def admin_content_upper_music_link_delete_post():

    upper_content_music_id = request.form.get('upper_content_music_id')
    proc = 'uspSetStreamAdminContentUpperMusicLinkDelete @UpperContentMusicID=?'
    conn.execute_without_return(proc, upper_content_music_id)

    return jsonify({"result": "success"})


# 교재 기반 첨부파일 (교사용)
@bp.route("/admin_content_reference_list"
           "/<int:route_kind_id>/<int:product_kind_id>/<int:content_title_id>", methods=['GET'])
@admin_required
def admin_content_reference_list(route_kind_id, product_kind_id, content_title_id):
    proc_title = "uspGetStreamAdminContentTitleInfo @ContentTitleID=?"
    content_title = conn.execute_return(proc_title, content_title_id).ContentTitle

    proc = 'uspGetStreamContentTitleInfoManager @ContentTitleID=?'
    res = conn.execute_return(proc, content_title_id)

    proc_list = 'uspGetStreamAdminContentReferenceList @ContentTitleID=?'
    res_list = conn.return_list(proc_list, content_title_id)

    return render_template('products/admin_content_reference_list.html', res=res, res_list=res_list
                           , route_kind_id=route_kind_id, product_kind_id=product_kind_id
                           , content_title_id=content_title_id, content_title=content_title)


@bp.route("/admin_content_reference_title_insert", methods=['POST'])
@admin_required
def admin_content_reference_title_insert():
    member_id = session['login_user']['member_id']
    content_title_id = int(request.form.get("content_title_id"))
    refe_kind_id = int(request.form.get("refe_kind_id"))
    title = request.form.get("title")

    proc = 'uspSetStreamAdminContentReferenceTitleInsert @MemberID=?, @ContentTitleID=?, @RefeKindID=?, @Title=?'
    params = [member_id, content_title_id, refe_kind_id, title]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_reference_title_update", methods=['POST'])
@admin_required
def admin_content_reference_title_update():
    member_id = session['login_user']['member_id']
    content_reference_id = int(request.form.get("content_reference_id"))
    refe_kind_id = int(request.form.get("refe_kind_id"))
    title = request.form.get("title")

    proc = "uspSetStreamAdminContentReferenceTitleUpdate @ContentReferenceID=?, @MemberID=?, @RefeKindID=?, @Title=?"
    params = [content_reference_id, member_id, refe_kind_id, title]
    conn.execute_without_return(proc, params)

    return jsonify({"result": "success"})


@bp.route("/admin_content_reference_display_update", methods=['POST'])
@admin_required
def admin_content_reference_display_update():
    content_reference_id = request.form.get('content_reference_id')
    display_yn = request.form.get('display_yn')

    proc = 'uspSetStreamAdminContentReferenceDisplayYn @ContentReferenceID=?, @DisplayYn=?'
    conn.execute_without_return(proc, [content_reference_id, display_yn])

    return jsonify({"result": "success"})


@bp.route("/admin_content_reference_delete", methods=['POST'])
@admin_required
def admin_content_reference_delete():
    content_reference_id = request.form.get('content_reference_id')
    proc = 'uspSetStreamAdminContentReferenceDelete @ContentReferenceID=?'
    conn.execute_without_return(proc, content_reference_id)

    return jsonify({"result": "success"})


@bp.route("/admin_content_reference_file_delete", methods=['POST'])
@admin_required
def admin_content_reference_file_delete():
    content_reference_id = request.form.get('content_reference_id')
    proc = 'uspSetStreamAdminContentReferenceFileDelete @ContentReferenceID=?'
    conn.execute_without_return(proc, content_reference_id)

    return jsonify({"result": "success"})


@bp.route("/admin_content_reference_file_upload", methods=['POST'])
@admin_required
def admin_content_reference_file_upload():
    content_title_id = request.form.get('content_title_id')
    content_reference_id = request.form.get('content_reference_id')
    member_id = session['login_user']['member_id']

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], "ContentReference", content_title_id)
    upload_files = request.files.getlist('image_file')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamAdminContentReferenceFileUpload \
              @ContentReferenceID=?, @MemberID=?, @UploadFilePath=?, @UploadFileName=?'
    params = [content_reference_id, member_id, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return jsonify({"file_name": file_name_str})


@bp.route("/admin_content_reference_sort_update", methods=['POST'])
@admin_required
def admin_content_reference_sort_update():
    ids = request.json.get('content_reference_ids')
    proc = 'uspSetStreamAdminContentReferenceSortUpdate @ContentReferenceID=?, @OrderNum=?'
    for num, i in enumerate(ids):
        conn.execute_without_return(proc, [i, num+1])

    return jsonify({"result": "success"})


@bp.route("/admin_content_reference_comment_update", methods=['POST'])
@admin_required
def admin_content_reference_comment_update():
    content_reference_id = request.form.get("content_reference_id")
    comments = request.form.get("comments")

    proc = 'uspSetStreamContentReferenceCommentUpdate @ContentReferenceID=?, @Comments=?'
    conn.execute_without_return(proc, [content_reference_id, comments])

    return jsonify({"result": "success"})


# 화상수업용 슬라이드 (교사용)
@bp.route("/content_booklet_list/<int:product_kind_id>/<int:content_title_id>/<int:booklet_id>", methods=['GET'])
@login_required
def content_booklet_list(product_kind_id, content_title_id, booklet_id):
    proc_booklet = "uspGetStreamAdminContentBookletList @ContentTitleID=?"
    booklet_list = conn.return_list(proc_booklet, content_title_id)

    if booklet_id == 0:
        if booklet_list:
            first_row = booklet_list[0]
            booklet_id = first_row[0]

    proc = "uspGetStreamAdminContentBookletSubList @BookletID=?"
    res_list = conn.return_list(proc, booklet_id)

    return render_template('products/content_booklet_list.html',
                           product_kind_id=product_kind_id, content_title_id=content_title_id,
                           booklet_id=booklet_id, booklet_list=booklet_list, res_list=res_list)


@bp.route("/content_booklet_sample_list/<int:product_kind_id>/<int:board_kind_id>/<product_kind>", methods=['GET'])
@login_required
def content_booklet_sample_list(product_kind_id, board_kind_id, product_kind):
    proc = "uspGetStreamContentBookletSampleList @ProductKind=?"
    res_list = conn.return_list(proc, product_kind)

    return render_template('products/content_booklet_sample_list.html', product_kind_id=product_kind_id
                           , board_kind_id=board_kind_id, product_kind=product_kind, res_list=res_list)


@bp.route("/admin_content_booklet_list/<int:route_kind_id>/<int:product_kind_id>/"
           "<int:content_title_id>/<int:booklet_kind_id>", defaults={'booklet_kind_id': 0}, methods=['GET'])
@admin_required
def admin_content_booklet_list(route_kind_id, product_kind_id, content_title_id, booklet_kind_id):

    proc_title = "uspGetStreamAdminContentTitleInfo @ContentTitleID=?"
    content_title = conn.execute_return(proc_title, content_title_id).ContentTitle

    booklet_kind_id = booklet_kind_id or BookletKind.STORY_BOOK.value

    proc_booklet = "uspGetStreamAdminContentBookletID @ContentTitleID=?, @BookletKindID=?"
    booklet_id = conn.execute_return(proc_booklet, [content_title_id, booklet_kind_id]).BookletID

    proc_list = "uspGetStreamAdminContentBookletSubList @BookletID=?"
    res_list = conn.return_list(proc_list, booklet_id)

    return render_template('products/admin_content_booklet_list.html',res_list=res_list
                           , booklet_kind_id=booklet_kind_id, route_kind_id=route_kind_id
                           , product_kind_id=product_kind_id, booklet_id=booklet_id
                           , content_title_id=content_title_id, content_title=content_title)


@bp.route("/admin_content_booklet_file_insert", methods=['POST'])
@admin_required
def admin_content_booklet_sub_insert():
    booklet_id = request.form.get('booklet_id')
    member_id = session['login_user']['member_id']
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Booklet', booklet_id)
    upload_files = request.files.getlist('image_file')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamAdminContentBookletSubInsert @BookletID=?, @MemberID=?, @UploadFilePath=?, @UploadFileName=?'
    params = [booklet_id, member_id, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return jsonify({"file_name": file_name_str})


@bp.route("/admin_content_booklet_image_upload", methods=['POST'])
@admin_required
def admin_content_booklet_image_upload():
    booklet_id = request.form.get('booklet_id')
    member_id = session['login_user']['member_id']

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Booklet', booklet_id)
    upload_files = request.files.getlist('image_files')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamAdminContentBookletFileUpload @BookletID=?, @MemberID=?, @UploadFilePath=?, @FileNameString=?'
    params = [booklet_id, member_id, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return jsonify({"file_name": file_name_str})


@bp.route("/admin_content_booklet_sub_image_upload", methods=['POST'])
@admin_required
def admin_content_booklet_sub_image_upload():
    booklet_id = request.form.get('booklet_id')
    booklet_sub_id = request.form.get('booklet_sub_id')
    member_id = session['login_user']['member_id']

    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'Booklet', booklet_id)
    upload_files = request.files.getlist('image_file')

    file_handler = FileHandler(upload_path)
    file_name_str = file_handler.file_upload(upload_files)

    proc = 'uspSetStreamAdminContentBookletSubFileUpload @BookletSubID=?, @MemberID=?, @UploadFilePath=?, @UploadFileName=?'
    params = [booklet_sub_id, member_id, upload_path, file_name_str]
    conn.execute_without_return(proc, params)

    return jsonify({"file_name": file_name_str})


@bp.route("/admin_content_booklet_sub_sort_update", methods=['POST'])
@admin_required
def admin_content_booklet_sub_sort_update():
    ids = request.json.get('booklet_sub_ids')
    proc = 'uspSetStreamAdminContentBookletSubSortUpdate @BookletSubID=?, @OrderNum=?'
    for num, i in enumerate(ids):
        conn.execute_without_return(proc, [i, num+1])

    return jsonify({"result": "success"})


@bp.route("/admin_content_booklet_sub_display_update", methods=['POST'])
@admin_required
def admin_content_booklet_sub_display_update():
    display_yn = request.form.get('display_yn')
    booklet_sub_id = request.form.get("booklet_sub_id")

    proc = 'uspSetStreamAdminContentBookletSubDisplayYn @BookletSubID=?, @DisplayYn=?'
    conn.execute_without_return(proc, [booklet_sub_id, display_yn])

    return jsonify({"result": "success"})


@bp.route("/admin_content_booklet_sub_delete", methods=['POST'])
@admin_required
def admin_content_booklet_sub_delete():
    booklet_sub_id = request.form.get("booklet_sub_id")
    proc = 'uspSetStreamAdminContentBookletSubDelete @BookletSubID=?'
    conn.execute_without_return(proc, booklet_sub_id)

    return jsonify({"result": "success"})
