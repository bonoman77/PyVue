from flask import current_app, render_template
from flask_mail import Mail, Message

BRAND_NAME = "튼튼플레이어"
AUTH_HEAD_URL = "https://player.tuntun.com/accounts"


def send_mail(user_mail, member_name, auth_code, format_type):

    mail = Mail(current_app)
    msg = Message()

    if format_type == 'reset_passwd':
        auth_url = f"{AUTH_HEAD_URL}/auth_pass_update?user_email={user_mail}&auth_code={auth_code}"
    else:
        auth_url = f"{AUTH_HEAD_URL}/auth?user_email={user_mail}&auth_code={auth_code}"

    subject_mapping = {
        'register': f"{BRAND_NAME} 가입을 환영합니다.",
        're_auth': f"{BRAND_NAME} 이메일 재인증 안내입니다.",
        'update_email': f"{BRAND_NAME} 이메일 계정 변경 안내입니다.",
        'reset_passwd': f"{BRAND_NAME} 비밀번호 초기화 안내입니다."
    }

    subject = subject_mapping.get(format_type, "에러 발생")
    msg.subject = subject
    msg.recipients = [user_mail]

    html_content = render_template('emails/auth_format.html', format_type=format_type, member_name=member_name, auth_url=auth_url)
    msg.html = html_content

    try:
        mail.send(msg)
        current_app.logger.info("메일 발송 성공: %s", user_mail)
    except Exception as e:
        current_app.logger.error(f"메일 발송 오류: {str(e)}", exc_info=True)
