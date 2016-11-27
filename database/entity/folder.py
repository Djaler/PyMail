from peewee import *

from database.entity.account import Account
from database.entity.base_entity import BaseEntity


class Folder(BaseEntity):
    name = TextField()
    parent = ForeignKeyField('self', null=True, related_name='folders')
    account = ForeignKeyField(Account, related_name="folders")
    with_emails = BooleanField(default=True)
