import keyring
from peewee import *

from model.account import Account
from model.base_entity import BaseEntity


class PublicKey(BaseEntity):
    account = ForeignKeyField(Account, related_name="public_keys")
    address = TextField()
    
    def __init__(self, *args, key=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if key:
            self._key = key
    
    def save(self, force_insert=False, only=None):
        if super().save(force_insert, only):
            keyring.set_password("PyMailPublicKeys",
                                 self.account.address + " " + self.address,
                                 self._key)
    
    @property
    def key(self):
        return keyring.get_password("PyMailPublicKeys",
                                    self.account.address + " " + self.address)
    
    class Meta:
        db_table = 'public_keys'
