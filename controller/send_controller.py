from controller.base_controller import BaseController
from crypto import cipher
from mail import smtp
from model import ForeignKey


class SendController(BaseController):
    def __init__(self, current_account):
        super().__init__()
        self._current_account = current_account
    
    def send(self):
        body = self._view.body

        address = self._view.to

        public_key = self._current_account.foreign_keys.where(
            ForeignKey.address == address)

        if public_key.exists():
            body = cipher.encrypt(body, public_key.get().key)
        
        try:
            smtp.send(self._current_account, address, self._view.subject, body)
        except smtp.IncorrectAddress:
            self._view.show_error("Введён некорректный адрес")
        except smtp.EmptyBody:
            self._view.show_error("Тело письма не должно быть пустым")
        else:
            self._view.accept()
