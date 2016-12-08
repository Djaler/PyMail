import keyring

from crypto import rsa


def generate(account):
    public, private = rsa.generate_keys()
    
    keyring.set_password("PyMail", account + " public", public)
    keyring.set_password("PyMail", account + " private", private)


def get_keys(account):
    public = keyring.get_password("PyMail", account + " public")
    private = keyring.get_password("PyMail", account + " private")
    
    return public, private
