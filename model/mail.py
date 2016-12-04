from peewee import *

from model.base_entity import BaseEntity
from model.folder import Folder


class Mail(BaseEntity):
    uid = IntegerField()
    folder = ForeignKeyField(Folder, related_name="mails")
    body = TextField(null=True)
    subject = TextField(null=True)
    recipient = TextField()
    sender = TextField()
    datetime = DateTimeField()
    is_html = BooleanField()

    class Meta:
        db_table = 'mails'
