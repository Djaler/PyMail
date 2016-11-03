from models.database import database
from models.entities.account import Account
from models.entities.folder import Folder
from models.entities.mail import Mail
from models.entities.attachment import Attachment


def init_database(address):
    database.init(address)
    
    database.connect()
    database.create_tables([Account, Folder, Mail, Attachment], True)
