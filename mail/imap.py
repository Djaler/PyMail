import imapy
from imapy.imap import *
from peewee import SelectQuery

from database.entity import Account


@is_logged
def folder(self, folder_name=''):
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


IMAP.folder = folder


class ImapService:
    def __init__(self):
        self._accounts = []
        self._connections = []
    
    def set_accounts(self, accounts: SelectQuery):
        self._accounts = list(accounts)
    
    def add_account(self, account: Account):
        self._accounts.append(account)
    
    @staticmethod
    def _connect(account: Account):
        return imapy.connect(host=account.imap_host, port=account.imap_port,
                             username=account.address,
                             password=account.password, ssl=account.imap_ssl)
    
    def connect_all(self):
        self._connections.clear()
        self._connections.extend(map(self._connect, self._accounts))
    
    def get_connections(self):
        return self._connections

    def logout(self):
        for connection in self._connections:
            connection.logout()
