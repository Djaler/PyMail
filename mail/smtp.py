from smtplib import SMTPRecipientsRefused

from outbox import Outbox, Email

from model import Account


class SendService:
    def __init__(self, account: Account):
        self._account = account
    
    def __enter__(self):
        self._connection = Outbox(server=self._account.smtp_host,
                                  port=self._account.smtp_port,
                                  username=self._account.address,
                                  password=self._account.password,
                                  mode='SSL' if self._account.smtp_ssl else
                                  None)
        self._connection.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.disconnect()
    
    def send(self, to, subject, body):
        if not body:
            raise EmptyBody
        
        email = Email(recipients=to, subject=subject, body=body)
        
        try:
            self._connection.send(email)
        except SMTPRecipientsRefused:
            raise IncorrectAddress


class IncorrectAddress(Exception):
    pass


class EmptyBody(Exception):
    pass
