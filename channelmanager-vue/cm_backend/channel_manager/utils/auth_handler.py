from flask import request, session, redirect, url_for
from functools import wraps
import channel_manager.dbconns as conn

LOGIN_ENDPOINT = 'accounts.login'
FAILED_ENDPOINT = 'homes.message'
ADMIN_CHECK_PROC = 'uspGetChannelAdminYn'


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

        user_id = login_user['user_id']

        if not is_admin(user_id):
            return redirect(url_for(FAILED_ENDPOINT, msg_kind="route_error"))

        return func(*args, **kwargs)

    return decorated_function


def is_admin(user_id):
    admin_yn = bool(conn.execute_return(f'{ADMIN_CHECK_PROC} @UserID=?', user_id).AdminYn)
    return admin_yn

