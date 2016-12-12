from controller import BaseController


class ChangeAccountController(BaseController):
    def __init__(self, current_account, main_controller):
        super().__init__()
        self._current_account = current_account
        self._main_controller = main_controller
    
    def set_account_info(self):
        self._view.set_account_info(name=self._current_account.name,
                                    address=self._current_account.address,
                                    password=self._current_account.password,
                                    imap_host=self._current_account.imap_host,
                                    imap_port=self._current_account.imap_port,
                                    imap_ssl=self._current_account.imap_ssl,
                                    smtp_host=self._current_account.smtp_host,
                                    smtp_port=self._current_account.smtp_port,
                                    smtp_ssl=self._current_account.smtp_ssl)
    
    def apply(self):
        self._current_account.name = self._view.name
        self._current_account.address = self._view.address
        self._current_account.password = self._view.password
        self._current_account.imap_host = self._view.imap_host
        self._current_account.imap_port = self._view.imap_port
        self._current_account.imap_ssl = self._view.imap_ssl
        self._current_account.smtp_host = self._view.smtp_host
        self._current_account.smtp_port = self._view.smtp_port
        self._current_account.smtp_ssl = self._view.smtp_ssl
        
        self._current_account.save()
        
        self._view.accept()
    
    def delete(self):
        self._current_account.delete_instance(recursive=True)
        
        self._main_controller.update_accounts()
        
        self._view.accept()
