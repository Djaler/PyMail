import re
from collections import OrderedDict

from controller.base_controller import BaseController
from database.entity import Folder, Mail
from mail.mailer import Mailer


class MainController(BaseController):
    def __init__(self):
        super().__init__()
        self._mailer = Mailer()
    
    def sync(self):
        accounts = OrderedDict()

        self._mailer.sync()
        for account in self._mailer.get_accounts():
            # for account in Account.select():
            accounts[account.address] = OrderedDict()
            
            def load_children(parent_folder, parent_node):
                for child in parent_folder.folders:
                    parent_node[child.name] = OrderedDict()
                    
                    load_children(child, parent_node[child.name])
            
            for folder in account.folders.select().where(
                    Folder.parent.is_null()):
                accounts[account.address][folder.name] = OrderedDict()
                
                load_children(folder, accounts[account.address][folder.name])
        
        self._view.update_folders_tree(accounts)

        self._view.select_first_folder()
    
    def folder_changed(self):
        self._view.clear_mails_widget()
        
        folder_name = self._view.current_folder
        
        try:
            current_folder = Folder.select().where(
                (Folder.name == folder_name) & (Folder.with_emails == 1))[0]
        except IndexError:
            return
        
        emails = Mail.select().where(Mail.folder == current_folder).order_by(
            Mail.uid.desc())
        
        for email in emails:
            self._view.add_mail(email)

        self._view.select_first_mail()
    
    def mail_changed(self):
        current_id = self._view.current_mail_id
        
        current_mail = Mail.get(Mail.id == current_id)

        from_ = current_mail.sender
        to = current_mail.recipient
        subject = current_mail.subject
        
        body = current_mail.body
        if not current_mail.is_html:
            body = "<br/>\n".join(body.splitlines())
            
            url_pattern = re.compile(
                '((https?://)?([\w.]+)\.([a-z]{2,6}\.?)(/[^\s]*)*/?)')
            
            body = url_pattern.sub(r'<a href="\1">\1</a>', body)

        self._view.set_mail(from_, to, subject, body)
