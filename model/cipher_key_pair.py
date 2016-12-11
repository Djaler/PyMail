import keyring
from peewee import *

from model.account import Account
from model.base_entity import BaseEntity


class CipherKeyPair(BaseEntity):
    account = ForeignKeyField(Account, related_name="cipher_key_pairs")
    address = TextField()
    
    def __init__(self, *args, public=None, private=None, **kwargs):
        super().__init__(*args, **kwargs)

        if public:
            self._public = public

        if private:
            self._private = private
    
    def save(self, force_insert=False, only=None):
        if super().save(force_insert, only):
            keyring.set_password("PyMail",
                                 self.account.address + " " + self.address +
                                 " cipher public",
                                 self._public)

            keyring.set_password("PyMail",
                                 self.account.address + " " + self.address + " cipher private",
                                 self._private)
    
    @property
    def public_key(self):
        return keyring.get_password("PyMail",
                                    self.account.address + " " + self.address + " cipher public")
    
    @property
    def private_key(self):
        return keyring.get_password("PyMail",
                                    self.account.address + " " + self.address + " cipher private")
    
    class Meta:
        db_table = 'cipher_key_pairs'
        
        indexes = ((('account', 'address'), True),)
