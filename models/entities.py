from datetime import date

from pony.orm import *

_db = Database()


class Account(_db.Entity):
    _table_ = 'accounts'
    id = PrimaryKey(int, auto=True)
    address = Required(str, unique=True)
    password = Required(str)
    name = Required(str)
    imap_host = Required(str)
    imap_port = Required(int)
    imap_ssl = Required(bool)
    smtp_host = Required(str)
    smtp_port = Required(int)
    smtp_ssl = Required(bool)
    last_sync = Optional(date)
    folders = Set('Folder')


class Folder(_db.Entity):
    _table_ = 'folders'
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    account = Required(Account)
    mails = Set('Mail')


class Mail(_db.Entity):
    _table_ = 'mails'
    id = PrimaryKey(int, auto=True)
    folder = Required(Folder, column='folder_id')
    body = Optional(str)
    subject = Optional(str)
    recipient = Required(str)
    sender = Required(str)
    attachments = Set('Attachment')


class Attachment(_db.Entity):
    _table_ = 'attachments'
    id = PrimaryKey(int, auto=True)
    mail = Required(Mail, column='mail_id')
    path = Required(str)


def init_database(address):
    _db.bind("sqlite", "../" + address, create_db=True)
    _db.generate_mapping(create_tables=True)
