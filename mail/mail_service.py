import base64
import email
import locale
import quopri
import re
import sys
from datetime import datetime, timedelta

import easyimap
from imapy import utils

from database.entity import Folder, Mail

_charset_pattern = re.compile('charset\s*=\s*"?([\w-]+)"?')


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

            try:
                encoding = _charset_pattern.search(mail.content_type).group(1)
            except (IndexError, AttributeError):
                encoding = "utf-8"
            raw_mail = email.message_from_string(mail.raw.decode(encoding))
            body, is_html = _get_body(raw_mail)
            
            Mail.create(uid=id_, folder=folder, body=body, subject=mail.title,
                        recipient=mail.to, sender=mail.from_addr,
                        datetime=mail.date, is_html=is_html)
    connection.quit()


def _get_body(message):
    is_html = True
    for part in message.walk():
        if part.get_content_type() == 'text/html':
            body_part = part
            break
    else:
        for part in message.walk():
            if part.get_content_type() == 'text/plain':
                body_part = part
                is_html = False
                break
        else:
            raise Exception("Something happened.")
    
    body = body_part.get_payload()
    
    if body_part.get("Content-Transfer-Encoding") == "quoted-printable":
        try:
            body = quopri.decodestring(body)
            encoding = _charset_pattern.search(
                body_part.get("Content-Type")).group(1)
            body = body.decode(encoding)
        except ValueError:
            pass
    
    if body_part.get("Content-Transfer-Encoding") == "base64":
        body = base64.b64decode(body)
        encoding = _charset_pattern.search(
            body_part.get("Content-Type")).group(1)
        body = body.decode(encoding)
    
    return body, is_html


def _to_utf_7(name):
    return utils.b('"') + utils.str_to_utf7(name) + utils.b('"')
