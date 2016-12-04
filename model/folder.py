from peewee import *

from model.account import Account
from model.base_entity import BaseEntity


class Folder(BaseEntity):
    name = TextField()
    parent = ForeignKeyField('self', null=True, related_name='folders')
    account = ForeignKeyField(Account, related_name="folders")
    with_emails = BooleanField(default=True)

    class Meta:
        db_table = 'folders'
    
        indexes = ((('name', 'parent', 'account'), True),)
