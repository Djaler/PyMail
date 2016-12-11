import keyring
from peewee import *
from playhouse.signals import *

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
    
    @property
    def public_key(self):
        return keyring.get_password("PyMail",
                                    self.account.address + " " +
                                    self.address + " cipher public")
    
    @property
    def private_key(self):
        return keyring.get_password("PyMail",
                                    self.account.address + " " +
                                    self.address + " cipher private")
    
    class Meta:
        db_table = 'cipher_key_pairs'
        
        indexes = ((('account', 'address'), True),)


@post_save(sender=CipherKeyPair)
def on_save_handler_cipher_pair(model_class, instance, created):
    keyring.set_password("PyMail",
                         instance.account.address + " " + instance.address +
                         " cipher public",
                         instance._public)
    
    keyring.set_password("PyMail",
                         instance.account.address + " " + instance.address +
                         " cipher private",
                         instance._private)


@pre_delete(sender=CipherKeyPair)
def on_delete_handler_cipher_pair(model_class, instance):
    keyring.delete_password("PyMail",
                            instance.account.address + " " +
                            instance.address + " cipher public")
    
    keyring.delete_password("PyMail",
                            instance.account.address + " " +
                            instance.address + " cipher private")
