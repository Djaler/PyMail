import keyring
from peewee import *

from database.entity.base_entity import BaseEntity


class Account(BaseEntity):
    name = TextField()
    address = TextField(unique=True)
    imap_host = TextField()
    imap_port = IntegerField()
    imap_ssl = BooleanField()
    smtp_host = TextField()
    smtp_port = IntegerField()
    smtp_ssl = BooleanField()
    last_sync = DateTimeField(null=True)
    
    def __init__(self, *args, password=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if password:
            self._password = password
    
    def save(self, force_insert=False, only=None):
        if super().save(force_insert, only):
            keyring.set_password("PyMail", self.address, self._password)
    
    @property
    def password(self):
        return keyring.get_password("PyMail", self.address)

    class Meta:
        db_table = 'accounts'
