from peewee import *

from models.entities.base_entity import BaseEntity
from models.entities.account import Account


class Folder(BaseEntity):
    name = TextField(unique=True)
    account = ForeignKeyField(Account, related_name="folders")
