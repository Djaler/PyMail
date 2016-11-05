from peewee import *

from database import database


class BaseEntity(Model):
    id = PrimaryKeyField()
    
    class Meta:
        database = database
