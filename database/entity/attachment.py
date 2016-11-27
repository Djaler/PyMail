from peewee import *

from database.entity.base_entity import BaseEntity
from database.entity.mail import Mail


class Attachment(BaseEntity):
    name = TextField(unique=True)
    mail = ForeignKeyField(Mail, related_name="attachments")
    path = TextField()

    class Meta:
        db_table = 'attachments'
