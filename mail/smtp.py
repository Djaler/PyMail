from smtplib import SMTPRecipientsRefused

from outbox import Outbox, Email

from model import Account


def send(account: Account, to: str, subject: str, body: str):
    if not body:
        raise EmptyBody
    
    connection = Outbox(server=account.smtp_host, port=account.smtp_port,
                        username=account.login, password=account.password,
                        mode='SSL' if account.smtp_ssl else None)
    connection.connect()
    
    email = Email(recipients=to, subject=subject, body=body)
    
    try:
        connection.send(email)
    except SMTPRecipientsRefused:
        raise IncorrectAddress


class IncorrectAddress(Exception):
    pass


class EmptyBody(Exception):
    pass
