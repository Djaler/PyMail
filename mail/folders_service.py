import imapy
from imapy.imap import *

from model import Account, Folder


@is_logged
def folder_(self, folder_name=''):
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


IMAP.folder = folder_


class FolderService:
    def __init__(self, account: Account):
        self._account = account
    
    def __enter__(self):
        self._connection = imapy.connect(host=self._account.imap_host,
                                         port=self._account.imap_port,
                                         username=self._account.address,
                                         password=self._account.password,
                                         ssl=self._account.imap_ssl)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.logout()
    
    def load_folders(self):
        folders = self._connection.folders()

        for folder in self._account.folders:
            if folder.name not in folders:
                folder.delete_instance(recursive=True)
    
        top_level_folders = [folder for folder in folders if
                             self._connection.separator not in folder]
        
        def load_children(parent_folder, parent_name):
            for child in self._connection.folder(parent_name).children():
                child_folder, _ = Folder.get_or_create(name=child,
                                                       account=self._account,
                                                       parent=parent_folder)
                
                if not self._connection.folder(child).info()['uidnext']:
                    child_folder.with_emails = False
                    child_folder.save()
                
                load_children(child_folder, child)
        
        for folder in top_level_folders:
            new_folder, _ = Folder.get_or_create(name=folder,
                                                 account=self._account)
            
            if not self._connection.folder(folder).info()['uidnext']:
                new_folder.with_emails = False
                new_folder.save()
            
            load_children(new_folder, folder)
