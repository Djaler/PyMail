from peewee import SqliteDatabase

database = SqliteDatabase(None)

from model.account import Account
from model.attachment import Attachment
from model.folder import Folder
from model.mail import Mail
from model.cipher_key_pair import CipherKeyPair
from model.cipher_foreign_key import CipherForeignKey
from model.signature_key_pair import SignatureKeyPair
from model.signature_foreign_key import SignatureForeignKey


def init_database(address):
    database.init(address)
    
    database.connect()
    database.create_tables(
        [Account, Folder, Mail, Attachment, CipherKeyPair, CipherForeignKey,
         SignatureKeyPair, SignatureForeignKey], True)
