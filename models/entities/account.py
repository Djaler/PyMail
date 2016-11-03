from peewee import *

from models.entities.base_entity import BaseEntity


class Account(BaseEntity):
    address = TextField(unique=True)
    password = TextField()
    name = TextField()
    imap_host = TextField()
    imap_port = IntegerField()
    imap_ssl = BooleanField()
    smtp_host = TextField()
    smtp_port = IntegerField()
    smtp_ssl = BooleanField()
    last_sync = DateTimeField(null=True)
