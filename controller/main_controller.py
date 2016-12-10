import re
import shutil
from collections import OrderedDict

from qtpy.QtCore import QObject

from controller import *
from crypto import cipher
from crypto.rsa import DecryptionError
from mail import imap
from model import *
from utils import save_dialog
from view import *


class MainController(QObject, BaseController):
    def __init__(self):
        super().__init__()

        self._accounts = list(Account.select())

        self._current_account = None

        self._current_mail = None
    
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
        imap.load(self._current_account)
        
        self._update()
    
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

        key_pair = self._current_account.key_pairs.where(
            KeyPair.address == from_)

        if key_pair.exists():
            try:
                body = cipher.decrypt(body, key_pair.get().private_key)
            except DecryptionError:
                pass
        
        attachments = {attach.name: attach.size for attach in
                       self._current_mail.attachments}

        self._view.set_mail(from_, to, subject, body, attachments)

    def save_attach(self):
        name = self.sender().text()

        path_to_save = save_dialog(self._view, name, "Сохранение файла")
        
        if not path_to_save:
            return

        original_path = list(self._current_mail.attachments.select().where(
            Attachment.name == name))[0].path

        shutil.copy(original_path, path_to_save)
    
    def send_mail(self):
        controller = SendController(self._current_account)
        dialog = SendDialog(controller)
        dialog.show()

    def import_public(self):
        controller = ImportPublicController(self._current_account)
        dialog = ImportPublicDialog(controller)
        dialog.show()

    def key_pairs(self):
        controller = KeyPairsController(self._current_account)
        dialog = KeyPairsDialog(controller)
        dialog.show()
