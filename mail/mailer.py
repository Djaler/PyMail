from database.entity import Account, Folder
from mail import folders_service, mail_service


class Mailer:
    def __init__(self):
        self._accounts = []
    
    def get_accounts(self):
        return self._accounts
    
    def sync(self):
        self._accounts = list(Account.select())
        for account in self._accounts:
            folders_service.load_folders(account)
    
        folders = Folder.select()
    
        for folder in folders:
            if folder.with_emails:
                mail_service.load_emails(folder)
