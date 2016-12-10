from controller import BaseController
from model import KeyPair
from utils import save_dialog


class ExportPublicController(BaseController):
    def __init__(self, current_account):
        super().__init__()
        self._current_account = current_account
    
    def export(self):
        key_pair = self._current_account.key_pairs.where(
            KeyPair.address == self._view.address)
        
        if key_pair.exists():
            public_key = key_pair.get().public_key
            
            name = self._view.address + ".key"
            path_to_save = save_dialog(self._view, name, "Экспорт ключа")
            
            if not path_to_save:
                return
            
            with open(path_to_save, "w") as file:
                file.write(public_key)
            
            self._view.accept()
