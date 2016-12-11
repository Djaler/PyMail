import keyring
from peewee import *
from playhouse.signals import *

from model.account import Account
from model.base_entity import BaseEntity


class SignatureForeignKey(BaseEntity):
    account = ForeignKeyField(Account, related_name="signature_foreign_keys")
    address = TextField()
    
    def __init__(self, *args, key=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if key:
            self._key = key
    
    @property
    def key(self):
        return keyring.get_password("PyMail",
                                    self.account.address + " " +
                                    self.address + " signature foreign public")
    
    class Meta:
        db_table = 'signature_foreign_keys'
        
        indexes = ((('account', 'address'), True),)


@post_save(sender=SignatureForeignKey)
def on_save_handler_sign_foreign(model_class, instance, created):
    keyring.set_password("PyMail",
                         instance.account.address + " " + instance.address +
                         " signature foreign public",
                         instance._key)


@pre_delete(sender=SignatureForeignKey)
def on_delete_handler_sign_foreign(model_class, instance):
    keyring.delete_password("PyMail",
                            instance.account.address + " " +
                            instance.address + " signature foreign public")
