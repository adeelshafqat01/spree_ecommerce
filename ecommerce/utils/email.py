from django.core.mail import send_mail


def send_email(reset_code, email, uid, passowrd):
    home_url = "http://127.0.0.1:8000"
    msg_title = "Reset your password."
    msg_contents = (
        f"Hello {email},\n"
        f"Your password was recently requested to be reset. "
        f"To confirm, go to\n"
        f"{home_url}/api/authenticate/resetpasswordhandler?code={reset_code}&uuid={uid}&pass={passowrd}\n\n"
        f"The link will expire in 5 minutes."
    )
    send_mail(msg_title, msg_contents, "admin@spree.com", [email])
