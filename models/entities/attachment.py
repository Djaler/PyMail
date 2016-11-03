from peewee import *

from models.entities.base_entity import BaseEntity
from models.entities.mail import Mail


class Attachment(BaseEntity):
    name = TextField(unique=True)
    mail = ForeignKeyField(Mail, related_name="attachments")
    path = TextField()
