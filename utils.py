import appdirs


def get_app_folder():
    return appdirs.user_data_dir("PyMail")
