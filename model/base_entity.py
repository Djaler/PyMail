from peewee import *

from model import database


class BaseEntity(Model):
    id = PrimaryKeyField()
    
    class Meta:
        database = database
