from database import database
from database.entity.account import Account
from database.entity.folder import Folder
from database.entity.mail import Mail
from database.entity.attachment import Attachment


def init_database(address):
    database.init(address)
    
    database.connect()
    database.create_tables([Account, Folder, Mail, Attachment], True)
