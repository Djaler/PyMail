from peewee import *

from database.entity.base_entity import BaseEntity
from database.entity.account import Account


class Folder(BaseEntity):
    name = TextField(unique=True)
    parent = ForeignKeyField('self', null=True, related_name='folders')
    account = ForeignKeyField(Account, related_name="folders")
