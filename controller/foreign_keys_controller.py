from qtpy.QtCore import QObject

from model import ForeignKey
from controller import BaseController, ImportPublicController
from view import ImportPublicDialog
from utils import save_dialog, open_dialog


class ForeignKeysController(QObject, BaseController):
    def __init__(self, current_account):
        super().__init__()
        
        self._current_account = current_account
    
    def load_keys(self):
        rows = [key.address for key in self._current_account.foreign_keys]
        self._view.set_rows(rows)
    
    def export(self):
        address = self.sender().property("address")
        
        key = self._current_account.foreign_keys.where(
            ForeignKey.address == address).get().key
        
        name = address + ".key"
        path_to_save = save_dialog(self._view, name, "Экспорт ключа")
        
        if not path_to_save:
            return
        
        with open(path_to_save, "w") as file:
            file.write(key)
    
    def import_(self):
        controller = ImportPublicController(self._current_account)
        dialog = ImportPublicDialog(controller)
        dialog.exec()
        
        self.load_keys()
