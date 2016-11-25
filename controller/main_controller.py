from collections import OrderedDict

from database.entity import Account, Folder, Mail
from mail.mailer import Mailer


class MainController:
    def __init__(self):
        self._view = None
        self._mailer = Mailer()
    
    def set_view(self, view):
        self._view = view
    
    def sync(self):
        accounts = OrderedDict()
        
        # self._mailer.sync()
        # for account in self._mailer.get_accounts():
        for account in Account.select():
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
    
    def mail_changed(self):
        current_id = self._view.current_mail_id
        
        current_mail = Mail.get(Mail.id == current_id)
        
        self._view.set_mail_body(current_mail.body)
