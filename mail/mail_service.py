import email
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

    past = datetime.now() - timedelta(weeks=2)
    
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
            mail = connection.mail(str(id_).encode(), include_raw=True)
    
            body = mail.body
            if r'\u' in body:
                raw_mail = email.message_from_string(mail.raw.decode('utf-8'))
                body = _get_body(raw_mail)
    
            Mail.create(uid=id_, folder=folder, body=body, subject=mail.title,
                        recipient=mail.to, sender=mail.from_addr,
                        datetime=mail.date)
    connection.quit()


def _get_body(message):
    for part in message.walk():
        maintype = part.get_content_maintype()
        if maintype != 'multipart' and not part.get_filename():
            return part.get_payload()
        if maintype == 'multipart':
            for p in part.get_payload():
                if p.get_content_maintype() == 'text':
                    return p.get_payload()
    raise Exception("Something happened.")


def _to_utf_7(name):
    return utils.b('"') + utils.str_to_utf7(name) + utils.b('"')
