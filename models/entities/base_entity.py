from peewee import *

from models.database import database


class BaseEntity(Model):
    id = PrimaryKeyField()
    
    class Meta:
        database = database
