from controller.base_controller import BaseController
from crypto import rsa
from model import SignatureKeyPair


class CreateKeysController(BaseController):
    def __init__(self, current_account):
        super().__init__()
        
        self._current_account = current_account
    
    def create(self):
        public, private = rsa.generate_keys()
        
        SignatureKeyPair.create(account=self._current_account,
                                address=self._view.address, public=public,
                                private=private)
        
        self._view.accept()
