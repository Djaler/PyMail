from controller import BaseController
from mail.mailer import send
from mail.smtp import EmptyBody, IncorrectAddress


class SendController(BaseController):
    def __init__(self, current_account):
        super().__init__()
        self._current_account = current_account
    
    def send(self):
        try:
            send(self._current_account, self._view.to, self._view.subject,
                 self._view.body)
        except IncorrectAddress:
            self._view.show_error("Введён некорректный адрес")
        except EmptyBody:
            self._view.show_error("Тело письма не должно быть пустым")
        else:
            self._view.accept()
