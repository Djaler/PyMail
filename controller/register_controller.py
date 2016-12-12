from controller import BaseController
from model import Account


class RegisterController(BaseController):
    def __init__(self, current_account=None, main_controller=None):
        super().__init__()
        self._current_account = current_account
        self._main_controller = main_controller
    
    def add(self):
        Account.create(name=self._view.name, address=self._view.address,
                       password=self._view.password,
                       imap_host=self._view.imap_host,
                       imap_port=self._view.imap_port,
                       imap_ssl=self._view.imap_ssl,
                       smtp_host=self._view.smtp_host,
                       smtp_port=self._view.smtp_port,
                       smtp_ssl=self._view.smtp_ssl)
        
        self._view.accept()

        if self._main_controller:
            self._main_controller.update_accounts()
