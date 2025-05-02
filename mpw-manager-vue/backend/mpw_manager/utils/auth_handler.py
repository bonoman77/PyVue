from flask import request, session, redirect, url_for
import mpw_manager.dbconns as conn
from functools import wraps

LOGIN_ENDPOINT = 'accounts.login'
FAILED_ENDPOINT = 'homes.message'
ADMIN_CHECK_PROC = 'uspGetStreamMemberAdminYn'


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not session.get('login_user'):
            session['next'] = request.url
            return redirect(url_for(LOGIN_ENDPOINT))
        return func(*args, **kwargs)
    return decorated_function


def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        login_user = session.get('login_user')
        if not login_user:
            session['next'] = request.url
            return redirect(url_for(LOGIN_ENDPOINT))

        member_id = login_user['member_id']

        if not is_admin(member_id):
            return redirect(url_for(FAILED_ENDPOINT, msg_kind="route_error"))

        return func(*args, **kwargs)

    return decorated_function


def is_admin(member_id):
    admin_yn = bool(conn.execute_return(f'{ADMIN_CHECK_PROC} @MemberID=?', member_id).AdminYn)
    return admin_yn

