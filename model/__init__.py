from peewee import SqliteDatabase

database = SqliteDatabase(None)

from model.account import Account
from model.attachment import Attachment
from model.folder import Folder
from model.mail import Mail
from model.key_pair import KeyPair
from model.foreign_key import ForeignKey


def init_database(address):
    database.init(address)
    
    database.connect()
    database.create_tables(
        [Account, Folder, Mail, Attachment, KeyPair, ForeignKey], True)
