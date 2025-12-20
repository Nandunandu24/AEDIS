import smtplib
from email.mime.text import MIMEText


def send_email_reply(
    to_email: str,
    subject: str,
    body: str,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_pass: str
):
    """
    Send email using SMTP.
    """

    msg = MIMEText(body)
    msg["From"] = smtp_user
    msg["To"] = to_email
    msg["Subject"] = subject

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(smtp_user, smtp_pass)
        server.send_message(msg)
