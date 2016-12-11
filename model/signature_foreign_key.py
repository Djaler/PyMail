import keyring
from peewee import *

from model.account import Account
from model.base_entity import BaseEntity


class SignatureForeignKey(BaseEntity):
    account = ForeignKeyField(Account, related_name="signature_foreign_keys")
    address = TextField()
    
    def __init__(self, *args, key=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if key:
            self._key = key
    
    def save(self, force_insert=False, only=None):
        if super().save(force_insert, only):
            keyring.set_password("PyMail",
                                 self.account.address + " " + self.address +
                                 " signature foreign public",
                                 self._key)
    
    @property
    def key(self):
        return keyring.get_password("PyMail",
                                    self.account.address + " " + self.address
                                    + " signature foreign public")
    
    class Meta:
        db_table = 'signature_foreign_keys'
        
        indexes = ((('account', 'address'), True),)
