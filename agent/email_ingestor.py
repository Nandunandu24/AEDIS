import imaplib
import email
from email.header import decode_header
from typing import List, Dict
from datetime import datetime


def fetch_unread_emails(
    imap_host: str,
    email_user: str,
    email_pass: str
) -> List[Dict]:
    """
    Fetch unread emails from inbox using IMAP.
    """

    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(email_user, email_pass)
    mail.select("inbox")

    status, messages = mail.search(None, "UNSEEN")
    email_data = []

    for num in messages[0].split():
        _, msg_data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        email_data.append({
            "email_id": num.decode(),
            "received_at": datetime.utcnow().isoformat(),
            "body": body.strip()
        })

    mail.logout()
    return email_data
