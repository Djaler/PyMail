from database.entity import *
from mail.imap import ImapService


class Mailer:
    def __init__(self):
        self._imap_service = ImapService()
        self._accounts = []
    
    def get_accounts(self):
        return self._accounts
    
    def sync(self):
        self._accounts = Account.select()
        
        self._imap_service.set_accounts(self._accounts)
        self._imap_service.connect_all()
        
        connections = self._imap_service.get_connections()
        
        for connection in connections:
            address = connection.username
            
            account = Account.get(address=address)
            
            self._sync_folders(connection, account)
        
        self._imap_service.logout()
    
    def _sync_folders(self, connection, account):
        # TODO Удаление из базы папок и писем, которых нет на сервере
        top_level_folders = [folder for folder in connection.folders() if
                             connection.separator not in folder]
        
        def load_children(parent_folder, parent_name):
            self._sync_mails(connection, parent_folder)
            
            for child in connection.folder(parent_name).children():
                child_folder, _ = Folder.create_or_get(name=child,
                                                       account=account,
                                                       parent=parent_folder)
                load_children(child_folder, child)
        
        for folder in top_level_folders:
            new_folder, _ = Folder.create_or_get(name=folder, account=account)
            load_children(new_folder, folder)
    
    def _sync_mails(self, connection, folder_entity):
        print(folder_entity.name)
        
        folder = connection.folder(folder_entity.name)
        if folder.info()['total'] is None:
            return
        
        emails = folder.emails(-5)
        
        if not emails:
            return
        
        print(len(emails))
        
        for email in emails:
            try:
                body = email['html'][0]
            except (KeyError, IndexError):
                body = email['text'][0]['text']
            
            Mail.create_or_get(folder=folder_entity, body=body,
                               subject=email['subject'], recipient=email['to'],
                               sender=email['from_email'])
