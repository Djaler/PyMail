from mail import FolderService, MailService


def sync(account):
    with FolderService(account) as folder_service:
        folder_service.load_folders()
    
    with MailService(account) as mail_service:
        for folder in account.folders:
            if folder.with_emails:
                mail_service.load_emails(folder)
