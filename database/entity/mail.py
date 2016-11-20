from peewee import *

from database.entity.base_entity import BaseEntity
from database.entity.folder import Folder


class Mail(BaseEntity):
    uid = IntegerField()
    folder = ForeignKeyField(Folder, related_name="mails")
    body = TextField(null=True)
    subject = TextField(null=True)
    recipient = TextField()
    sender = TextField()
    datetime = DateTimeField()
