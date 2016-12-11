from controller.base_controller import BaseController
from model import ForeignKey
from utils import open_dialog


class ImportPublicController(BaseController):
    def __init__(self, current_account):
        super().__init__()

        self._current_account = current_account
    
    def import_(self):
        path_to_open = open_dialog(self._view, "Импорт ключа")
        
        if not path_to_open:
            return
        
        with open(path_to_open) as file:
            public_key = file.read()
            
            ForeignKey.create(account=self._current_account,
                              address=self._view.address, key=public_key)
        
        self._view.accept()
