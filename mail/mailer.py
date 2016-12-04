from mail.imap import FolderService, MailService
from mail.smtp import SendService


def sync(account):
    with FolderService(account) as folder_service:
        folder_service.load_folders()
    
    with MailService(account) as mail_service:
        for folder in account.folders:
            if folder.with_emails:
                mail_service.load_emails(folder)


def send(account, to, subject, body):
    with SendService(account) as send_service:
        send_service.send(to, subject, body)
