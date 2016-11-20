import locale
import sys
from datetime import datetime, timedelta

import easyimap
from imapy import utils

from database.entity import Folder, Mail


def load_emails(folder: Folder):
    account = folder.account
    connection = easyimap.connect(host=account.imap_host,
                                  port=account.imap_port, user=account.address,
                                  password=account.password,
                                  ssl=account.imap_ssl)
    
    connection.change_mailbox(_to_utf_7(folder.name))
    
    past = datetime.now() - timedelta(weeks=4)
    
    locale.setlocale(locale.LC_TIME, ("en_US", "UTF-8"))
    date_criterion = '(SINCE "{}")'.format(past.strftime("%d-%b-%Y"))
    locale.resetlocale(locale.LC_TIME)
    
    ids_on_server = list(
        map(int, connection.listids(sys.maxsize, date_criterion)))
    
    Mail.delete().where(
        (Mail.folder == folder) & (Mail.uid.not_in(ids_on_server))).execute()
    
    local_ids = [mail.uid for mail in
                 Mail.select().where(Mail.folder == folder)]
    
    for id_ in ids_on_server:
        if id_ not in local_ids:
            mail = connection.mail(str(id_).encode())
            
            Mail.create(uid=id_, folder=folder, body=mail.body,
                        subject=mail.title, recipient=mail.to,
                        sender=mail.from_addr, datetime=mail.date)
    connection.quit()


def _to_utf_7(name):
    return utils.b('"') + utils.str_to_utf7(name) + utils.b('"')
