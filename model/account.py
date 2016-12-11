import keyring
from peewee import *
from playhouse.signals import *

from model.base_entity import BaseEntity


class Account(BaseEntity):
    name = TextField()
    address = TextField(unique=True)
    imap_host = TextField()
    imap_port = IntegerField()
    imap_ssl = BooleanField()
    smtp_host = TextField()
    smtp_port = IntegerField()
    smtp_ssl = BooleanField()
    
    def __init__(self, *args, password=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if password:
            self._password = password
    
    @property
    def password(self):
        return keyring.get_password("PyMail", self.address)

    class Meta:
        db_table = 'accounts'


@post_save(sender=Account)
def on_save_handler_account(model_class, instance, created):
    keyring.set_password("PyMail", instance.address, instance._password)


@pre_delete(sender=Account)
def on_delete_handler_account(model_class, instance):
    keyring.delete_password("PyMail", instance.address)
