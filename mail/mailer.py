from database.entity import Account
from mail import FolderService, MailService


class Mailer:
    def __init__(self):
        self._accounts = []
    
    def get_accounts(self):
        return self._accounts
    
    def sync(self):
        self._accounts = list(Account.select())
        for account in self._accounts:
            with FolderService(account) as folder_service:
                folder_service.load_folders()
    
            with MailService(account) as mail_service:
                for folder in account.folders:
                    if folder.with_emails:
                        mail_service.load_emails(folder)
