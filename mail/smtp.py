from smtplib import SMTPRecipientsRefused

from outbox import Outbox, Email, Attachment

from model import Account


def send(account: Account, to: str, subject: str, body: str, attachment,
         attachment_name):
    if not body:
        raise EmptyBody

    with Outbox(server=account.smtp_host, port=account.smtp_port,
                username=account.address, password=account.password,
                mode='SSL' if account.smtp_ssl else None) as connection:
    
        email = Email(recipients=to, subject=subject, body=body)
    
        attachments = []
    
        if attachment:
            attachments.append(Attachment(attachment_name, attachment))
    
        try:
            connection.send(email, attachments)
        except SMTPRecipientsRefused:
            raise IncorrectAddress


class IncorrectAddress(Exception):
    pass


class EmptyBody(Exception):
    pass
