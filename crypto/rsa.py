import rsa


def generate_keys():
    public_key, private_key = rsa.newkeys(512)
    
    return public_key, private_key


def encrypt(data, public_key):
    return rsa.encrypt(data, public_key)


def decrypt(data, private_key):
    try:
        return rsa.decrypt(data, private_key)
    except rsa.DecryptionError:
        raise DecryptionError


def sign(data, private_key):
    return rsa.sign(data, private_key, "SHA-256")


def verify(data, signature, public_key):
    try:
        rsa.verify(data, signature, public_key)
        return True
    except rsa.VerificationError:
        return False


class DecryptionError(Exception):
    pass
