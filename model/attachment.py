from peewee import *

from model.base_entity import BaseEntity
from model.mail import Mail


class Attachment(BaseEntity):
    name = TextField()
    mail = ForeignKeyField(Mail, related_name="attachments")
    path = TextField()
    size = IntegerField()

    class Meta:
        db_table = 'attachments'
