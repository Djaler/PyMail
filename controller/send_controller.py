import io
import os.path

from qtpy.QtWidgets import QMessageBox

from controller import BaseController
from crypto import cipher, signature
from mail import smtp
from model import CipherForeignKey, SignatureKeyPair
from utils import open_dialog


class SendController(BaseController):
    def __init__(self, current_account):
        super().__init__()
        self._current_account = current_account
    
    def send(self):
        body = self._view.body

        to = self._view.to

        body = self._encrypt_mail(body, to)

        attachment = None
        attachment_name = None

        attachment_path = self._view.attach
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                attachment = self._encrypt_attach(attachment.read(), to)
            attachment = io.BytesIO(attachment)
            attachment_name = os.path.basename(attachment_path)
        
        try:
            smtp.send(self._current_account, to, self._view.subject, body,
                      attachment, attachment_name)
        except smtp.IncorrectAddress:
            self._show_error("Введён некорректный адрес")
        except smtp.EmptyBody:
            self._show_error("Тело письма не должно быть пустым")
        else:
            self._view.accept()

    def _encrypt_attach(self, content, to):
        sign_private_key = self._current_account.signature_key_pairs.where(
            SignatureKeyPair.address == to)
        if sign_private_key.exists():
            content = signature.sign(content,
                                     sign_private_key.get().private_key)
    
        cipher_public_key = self._current_account.cipher_foreign_keys.where(
            CipherForeignKey.address == to)
        if cipher_public_key.exists():
            content = cipher.encrypt(content, cipher_public_key.get().key)
    
        return content

    def _encrypt_mail(self, body, to):
        sign_private_key = self._current_account.signature_key_pairs.where(
            SignatureKeyPair.address == to)
        if sign_private_key.exists():
            body = signature.sign(body.encode(),
                                  sign_private_key.get().private_key)
            body = body.decode()
    
        cipher_public_key = self._current_account.cipher_foreign_keys.where(
            CipherForeignKey.address == to)
        if cipher_public_key.exists():
            body = cipher.encrypt(body.encode(), cipher_public_key.get().key)
            body = body.decode()
    
        return body

    def attach_file(self):
        path_to_open = open_dialog(self._view, "Загрузка вложения")
    
        if path_to_open:
            self._view.set_attach(path_to_open)

    def _show_error(self, text):
        QMessageBox().warning(self, 'Ошибка', text)
