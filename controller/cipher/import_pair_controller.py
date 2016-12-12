from controller import BaseController
from model import CipherKeyPair
from utils import open_dialog


class ImportPairController(BaseController):
    def __init__(self, current_account):
        super().__init__()
        
        self._current_account = current_account
    
    def import_(self):
        path_to_open = open_dialog(self._view, "Импорт публичного ключа")
        
        if not path_to_open:
            return
        
        with open(path_to_open) as file:
            public_key = file.read()
        
        path_to_open = open_dialog(self._view, "Импорт приватного ключа")
        
        if not path_to_open:
            return
        
        with open(path_to_open) as file:
            private_key = file.read()
        
        CipherKeyPair.create(account=self._current_account,
                             address=self._view.address, public=public_key,
                             private=private_key)
        
        self._view.accept()
