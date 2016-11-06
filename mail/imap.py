import imapy
from peewee import SelectQuery

from database.entity import Account


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
