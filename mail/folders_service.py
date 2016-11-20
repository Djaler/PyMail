import imapy
from imapy.imap import *

from database.entity import Account, Folder


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


def load_folders(account: Account):
    # TODO Удаление папок, отсутствующих на сервере
    connection = imapy.connect(host=account.imap_host, port=account.imap_port,
                               username=account.address,
                               password=account.password, ssl=account.imap_ssl)
    
    top_level_folders = [folder for folder in connection.folders() if
                         connection.separator not in folder]
    
    def load_children(parent_folder, parent_name):
        for child in connection.folder(parent_name).children():
            child_folder, _ = Folder.create_or_get(name=child, account=account,
                                                   parent=parent_folder)
            
            if not connection.folder(child).info()['uidnext']:
                child_folder.with_emails = False
                child_folder.save()
            
            load_children(child_folder, child)
    
    for folder in top_level_folders:
        new_folder, _ = Folder.create_or_get(name=folder, account=account)
        
        if not connection.folder(folder).info()['uidnext']:
            new_folder.with_emails = False
            new_folder.save()
        
        load_children(new_folder, folder)
    
    connection.logout()
