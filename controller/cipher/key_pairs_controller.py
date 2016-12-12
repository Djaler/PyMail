from qtpy.QtCore import QObject

from controller import BaseController
from controller.cipher.create_keys_controller import CreateKeysController
from controller.cipher.import_pair_controller import ImportPairController
from model import CipherKeyPair
from utils import save_dialog
from view import CreateKeysDialog, ImportPairDialog


class CipherKeyPairsController(QObject, BaseController):
    def __init__(self, current_account):
        super().__init__()
        
        self._current_account = current_account
    
    def load_keys(self):
        rows = [pair.address for pair in
                self._current_account.cipher_key_pairs]
        self._view.set_rows(rows)
    
    def export_public(self):
        address = self.sender().property("address")

        public_key = self._current_account.cipher_key_pairs.where(
            CipherKeyPair.address == address).get().public_key
        
        self._export_key(public_key, address)
    
    def export_private(self):
        address = self.sender().property("address")

        private_key = self._current_account.cipher_key_pairs.where(
            CipherKeyPair.address == address).get().private_key
        
        self._export_key(private_key, address)
    
    def _export_key(self, key, address):
        name = address + ".key"
        path_to_save = save_dialog(self._view, name, "Экспорт ключа")
        
        if not path_to_save:
            return
        
        with open(path_to_save, "w") as file:
            file.write(key)
    
    def create_key_pair(self):
        controller = CreateKeysController(self._current_account)
        dialog = CreateKeysDialog(controller)
        dialog.exec()
        
        self.load_keys()

    def delete(self):
        address = self.sender().property("address")

        pair = self._current_account.cipher_key_pairs.where(
            CipherKeyPair.address == address).get()
        pair.delete_instance()

        self.load_keys()

    def import_key_pair(self):
        controller = ImportPairController(self._current_account)
        dialog = ImportPairDialog(controller)
        dialog.exec()
        
        self.load_keys()
