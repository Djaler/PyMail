import base64
import locale
import os
import quopri
import sys
from datetime import datetime, timedelta

import easyimap
import imapy
from imapy.imap import *

from model import Folder, Mail, Account, Attachment
from utils import get_app_folder


@is_logged
def _folder(self, folder_name=''):
    """Sets folder for folder-related operations. If folder_name is omitted
    then operations will be carried on topmost folder level."""
    if folder_name:
        if folder_name not in self.mail_folders:
            raise NonexistentFolderError(
                "The folder you are trying to select ({folder})"
                " doesn't exist".format(folder=folder_name))
        self.selected_folder = folder_name
        self.selected_folder_utf7 = utils.str_to_utf7(self.selected_folder)
        # select folder on server
        self.imap.select(
            utils.b('"') + self.selected_folder_utf7 + utils.b('"'))
        # get folder capabilities
        self._save_folder_capabilities(self.selected_folder)
    else:
        if self.selected_folder:
            self.imap.close()
        self.selected_folder = self.selected_folder_utf7 = None
    return self


IMAP.folder = _folder


def load(account: Account):
    try:
        _load_folders(account)
        
        with _MailService(account) as mail_service:
            for folder in account.folders:
                if folder.with_emails:
                    mail_service.load_emails(folder)
    except ConnectionRefused:
        raise SynchronizationError


def _load_folders(account: Account):
    connection = imapy.connect(host=account.imap_host, port=account.imap_port,
                               username=account.address,
                               password=account.password, ssl=account.imap_ssl)
    
    folders = connection.folders()
    
    for folder in account.folders:
        if folder.name not in folders:
            folder.delete_instance(recursive=True)
    
    top_level_folders = [folder for folder in folders if
                         connection.separator not in folder]
    
    def load_children(parent_folder, parent_name):
        for child in connection.folder(parent_name).children():
            child_folder, _ = Folder.get_or_create(name=child, account=account,
                                                   parent=parent_folder)
            
            if not connection.folder(child).info()['uidnext']:
                child_folder.with_emails = False
                child_folder.save()
            
            load_children(child_folder, child)
    
    for folder in top_level_folders:
        new_folder, _ = Folder.get_or_create(name=folder, account=account)
        
        if not connection.folder(folder).info()['uidnext']:
            new_folder.with_emails = False
            new_folder.save()
        
        load_children(new_folder, folder)
    
    connection.logout()


class _MailService:
    _charset_pattern = re.compile('charset\s*=\s*"?([\w-]+)"?')
    
    def __init__(self, account: Account):
        self._account = account
    
    def __enter__(self):
        self._connection = easyimap.connect(host=self._account.imap_host,
                                            port=self._account.imap_port,
                                            user=self._account.address,
                                            password=self._account.password,
                                            ssl=self._account.imap_ssl)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.quit()
    
    def load_emails(self, folder: Folder):
        self._connection.change_mailbox(self._to_utf_7(folder.name))

        date = datetime.now() - timedelta(weeks=2)

        date_criterion = self._create_date_criterion(date)

        ids_on_server = [int(id) for id in
                         self._connection.listids(sys.maxsize, date_criterion)]

        self._delete_mail_not_on_server(ids_on_server, folder, date)
        
        local_ids = [mail.uid for mail in
                     Mail.select().where(Mail.folder == folder)]
        
        for id_ in ids_on_server:
            if id_ in local_ids:
                continue
            mail = self._connection.mail(str(id_).encode(), include_raw=True)

            try:
                encoding = self._charset_pattern.search(
                    mail.content_type).group(1)
            except (IndexError, AttributeError):
                encoding = "utf-8"
            raw_mail = email.message_from_string(mail.raw.decode(encoding))
            body, is_html = self._get_body(raw_mail)
            subject = mail.title if mail.title else ''

            mail_instance = Mail.create(uid=id_, folder=folder, body=body,
                                        subject=subject, recipient=mail.to,
                                        sender=mail.from_addr,
                                        datetime=mail.date, is_html=is_html)

            self._load_attachments(mail_instance, mail)

    @staticmethod
    def _delete_mail_not_on_server(ids_on_server, folder, date):
        Mail.delete().where(
            (Mail.folder == folder) & (Mail.uid.not_in(ids_on_server)) & (
                Mail.datetime >= date)).execute()
    
    @staticmethod
    def _create_date_criterion(date):
        locale.setlocale(locale.LC_TIME, ("en_US", "UTF-8"))
        date_criterion = '(SINCE "{}")'.format(date.strftime("%d-%b-%Y"))
        locale.resetlocale(locale.LC_TIME)

        return date_criterion

    @staticmethod
    def _load_attachments(mail_instance, mail):
        for attachment in mail.attachments:
            name, content, _ = attachment

            path = os.path.join(get_app_folder(), "attachments",
                                str(mail_instance.folder.account.id),
                                str(mail_instance.id), name)

            Attachment.create(name=name, mail=mail_instance, path=path,
                              size=len(content))

            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as file:
                file.write(content)
    
    def _get_body(self, message):
        is_html = True
        for part in message.walk():
            if part.get_content_type() == 'text/html':
                body_part = part
                break
        else:
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    body_part = part
                    is_html = False
                    break
            else:
                raise Exception("Something happened.")
        
        body = body_part.get_payload()
        
        if body_part.get("Content-Transfer-Encoding") == "quoted-printable":
            try:
                body = quopri.decodestring(body)
                encoding = self._charset_pattern.search(
                    body_part.get("Content-Type")).group(1)
                body = body.decode(encoding)
            except ValueError:
                pass
        
        if body_part.get("Content-Transfer-Encoding") == "base64":
            body = base64.b64decode(body)
            encoding = self._charset_pattern.search(
                body_part.get("Content-Type")).group(1)
            body = body.decode(encoding)
        
        return body, is_html
    
    @staticmethod
    def _to_utf_7(name):
        return utils.b('"') + utils.str_to_utf7(name) + utils.b('"')


class SynchronizationError(Exception):
    pass
