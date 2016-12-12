import re
import shutil
from collections import OrderedDict
from threading import Thread

from qtpy.QtCore import QObject, Signal
from qtpy.QtWidgets import QMessageBox

from controller import (BaseController, CipherKeyPairsController,
                        CipherForeignKeysController, SendController,
                        SignatureKeyPairsController,
                        SignatureForeignKeysController,
                        ChangeAccountController, RegisterController)
from crypto import cipher, signature
from crypto.rsa import DecryptionError
from mail import imap
from model import *
from utils import save_dialog
from view import (ForeignKeysDialog, KeyPairsDialog, SendDialog,
                  ChangeAccountDialog, RegisterDialog)


class MainController(QObject, BaseController):
    _update_signal = Signal()
    _sync_fail_signal = Signal()
    
    def __init__(self):
        super().__init__()

        self._accounts = list(Account.select())

        self._current_account = None

        self._current_mail = None

        self._update_signal.connect(self._update)
        self._sync_fail_signal.connect(self._sync_fail)

    def update_accounts(self):
        self._accounts = list(Account.select())
        self.set_accounts()
    
    def _sync_fail(self):
        QMessageBox().warning(self._view, 'Ошибка', "Ошибка синхронизации")
    
    def account_changed(self, current_index):
        self._current_account = self._accounts[current_index]

        self._update()
    
    def _update(self):
        folders = OrderedDict()

        def load_children(parent_folder, parent_node):
            for child in parent_folder.folders:
                parent_node[child.name] = OrderedDict()

                load_children(child, parent_node[child.name])

        for folder in self._current_account.folders.select().where(
                Folder.parent.is_null()):
            folders[folder.name] = OrderedDict()

            load_children(folder, folders[folder.name])

        self._view.update_folders_tree(folders)
        
        self._view.select_first_folder()
    
    def set_accounts(self):
        self._view.set_accounts(account.name for account in self._accounts)
    
    def sync(self):
        Thread(target=self._sync).start()
    
    def _sync(self):
        try:
            imap.load(self._current_account)
        except imap.SynchronizationError:
            self._sync_fail_signal.emit()
        
        self._update_signal.emit()
    
    def folder_changed(self):
        self._view.clear_mails_widget()
        
        folder_name = self._view.current_folder
        
        try:
            current_folder = self._current_account.folders.select().where(
                (Folder.name == folder_name) & (Folder.with_emails == 1))[0]
        except IndexError:
            return
        
        emails = Mail.select().where(Mail.folder == current_folder).order_by(
            Mail.uid.desc())
        
        for email in emails:
            self._view.add_mail(email.id, email.sender, email.subject)
        
        self._view.select_first_mail()
    
    def mail_changed(self):
        current_id = self._view.current_mail_id

        self._current_mail = Mail.get(Mail.id == current_id)

        from_ = self._current_mail.sender
        to = self._current_mail.recipient
        subject = self._current_mail.subject

        body = self._current_mail.body
        if not self._current_mail.is_html:
            body = "<br/>\n".join(body.splitlines())
            
            url_pattern = re.compile(
                '((https?://)?([\w.]+)\.([a-z]{2,6}\.?)(/[^\s]*)*/?)')
            
            body = url_pattern.sub(r'<a href="\1">\1</a>', body)

        body = self._decrypt_mail(body, from_)

        attachments = {attach.name: attach.size for attach in
                       self._current_mail.attachments}

        self._view.set_mail(from_, to, subject, body, attachments)
    
    def _decrypt_mail(self, body, from_):
        cipher_key_pair = self._current_account.cipher_key_pairs.where(
            CipherKeyPair.address == from_)

        if cipher_key_pair.exists():
            try:
                body = cipher.decrypt(body.encode(),
                                      cipher_key_pair.get().private_key)
                body = body.decode()
            except DecryptionError:
                QMessageBox().warning(self._view, 'Ошибка',
                                      "Невозможно расшифровать")
                return body
        
        signature_key = self._current_account.signature_foreign_keys.where(
            SignatureForeignKey.address == from_)

        if signature_key.exists():
            body, correct = signature.decode_and_verify(body.encode(),
                                                        signature_key.get().key)
            body = body.decode()
            if not correct:
                QMessageBox().warning(self._view, 'Ошибка', "Подпись не верна")
        
        return body
    
    def save_attach(self):
        name = self.sender().text()

        path_to_save = save_dialog(self._view, name, "Сохранение файла")
        
        if not path_to_save:
            return

        original_path = list(self._current_mail.attachments.select().where(
            Attachment.name == name))[0].path

        encrypted = False
        content = None

        cipher_key_pair = self._current_account.cipher_key_pairs.where(
            CipherKeyPair.address == self._current_mail.sender)

        if cipher_key_pair.exists():
            encrypted = True

            with open(original_path, 'rb') as file:
                content = file.read()
            try:
                content = cipher.decrypt(content,
                                         cipher_key_pair.get().private_key)
            except DecryptionError:
                QMessageBox().warning(self._view, 'Ошибка',
                                      "Невозможно расшифровать")
                return
        
        signature_key = self._current_account.signature_foreign_keys.where(
            SignatureForeignKey.address == self._current_mail.sender)

        if signature_key.exists():
            if not encrypted:
                with open(original_path, 'rb') as file:
                    content = file.read()

            encrypted = True
            content, correct = signature.decode_and_verify(content,
                                                           signature_key.get().key)
            if not correct:
                QMessageBox().warning(self._view, 'Ошибка', "Подпись не верна")
                return
        
        if encrypted:
            with open(path_to_save, 'wb') as file:
                file.write(content)
        else:
            shutil.copy(original_path, path_to_save)
    
    def send_mail(self):
        controller = SendController(self._current_account)
        dialog = SendDialog(controller)
        dialog.show()
    
    def cipher_foreign_keys(self):
        controller = CipherForeignKeysController(self._current_account)
        dialog = ForeignKeysDialog(controller)
        dialog.show()
    
    def cipher_key_pairs(self):
        controller = CipherKeyPairsController(self._current_account)
        dialog = KeyPairsDialog(controller)
        dialog.show()
    
    def sign_foreign_keys(self):
        controller = SignatureForeignKeysController(self._current_account)
        dialog = ForeignKeysDialog(controller)
        dialog.show()
    
    def sign_key_pairs(self):
        controller = SignatureKeyPairsController(self._current_account)
        dialog = KeyPairsDialog(controller)
        dialog.show()

    def change_account(self):
        controller = ChangeAccountController(self._current_account, self)
        dialog = ChangeAccountDialog(controller)
        dialog.show()

    def add_account(self):
        controller = RegisterController(self._current_account, self)
        dialog = RegisterDialog(controller)
        dialog.show()
