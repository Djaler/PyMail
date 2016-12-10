import os.path

import appdirs
from qtpy.QtWidgets import QFileDialog


def get_app_folder():
    return appdirs.user_data_dir("PyMail")


def save_dialog(parent, name, title):
    home = os.path.expanduser("~")
    default_path = os.path.join(home, name)
    path_to_save, _ = QFileDialog().getSaveFileName(parent, title,
                                                    default_path)
    
    return path_to_save


def open_dialog(parent, title):
    home = os.path.expanduser("~")
    path_to_open, _ = QFileDialog().getOpenFileName(parent, title, home)
    
    return path_to_open
