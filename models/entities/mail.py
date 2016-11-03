from peewee import *

from models.entities.base_entity import BaseEntity
from models.entities.folder import Folder


class Mail(BaseEntity):
    folder = ForeignKeyField(Folder, related_name="mails")
    body = TextField(null=True)
    subject = TextField(null=True)
    recipient = TextField()
    sender = TextField()
