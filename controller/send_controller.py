from controller import BaseController
from crypto import cipher, signature
from mail import smtp
from model import CipherForeignKey, SignatureKeyPair


class SendController(BaseController):
    def __init__(self, current_account):
        super().__init__()
        self._current_account = current_account
    
    def send(self):
        body = self._view.body

        address = self._view.to

        sign_private_key = self._current_account.signature_key_pairs.where(
            SignatureKeyPair.address == address)
        if sign_private_key.exists():
            body = signature.sign(body, sign_private_key.get().private_key)

        cipher_public_key = self._current_account.cipher_foreign_keys.where(
            CipherForeignKey.address == address)
        if cipher_public_key.exists():
            body = cipher.encrypt(body, cipher_public_key.get().key)
        
        try:
            smtp.send(self._current_account, address, self._view.subject, body)
        except smtp.IncorrectAddress:
            self._view.show_error("Введён некорректный адрес")
        except smtp.EmptyBody:
            self._view.show_error("Тело письма не должно быть пустым")
        else:
            self._view.accept()
