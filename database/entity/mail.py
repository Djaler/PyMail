from peewee import *

from database.entity.base_entity import BaseEntity
from database.entity.folder import Folder


class Mail(BaseEntity):
    folder = ForeignKeyField(Folder, related_name="mails")
    body = TextField(null=True)
    subject = TextField(null=True)
    recipient = TextField()
    sender = TextField()
