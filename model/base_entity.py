from peewee import PrimaryKeyField
from playhouse.signals import Model

from model import database


class BaseEntity(Model):
    id = PrimaryKeyField()
    
    class Meta:
        database = database
