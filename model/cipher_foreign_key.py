import keyring
from peewee import *
from playhouse.signals import *

from model.account import Account
from model.base_entity import BaseEntity


class CipherForeignKey(BaseEntity):
    account = ForeignKeyField(Account, related_name="cipher_foreign_keys")
    address = TextField()
    
    def __init__(self, *args, key=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if key:
            self._key = key
    
    @property
    def key(self):
        return keyring.get_password("PyMail",
                                    self.account.address + " " +
                                    self.address + " cipher foreign public")
    
    class Meta:
        db_table = 'cipher_foreign_keys'
        
        indexes = ((('account', 'address'), True),)


@post_save(sender=CipherForeignKey)
def on_save_handler_cipher_foreign(model_class, instance, created):
    keyring.set_password("PyMail",
                         instance.account.address + " " + instance.address +
                         " cipher foreign public",
                         instance._key)


@pre_delete(sender=CipherForeignKey)
def on_delete_handler_cipher_foreign(model_class, instance):
    keyring.delete_password("PyMail",
                            instance.account.address + " " +
                            instance.address + " cipher foreign public")
