import rsa


def generate_keys():
    public_key, private_key = rsa.newkeys(512)

    return public_key.save_pkcs1(), private_key.save_pkcs1()


def encrypt(data, public_key):
    public_key = rsa.PublicKey.load_pkcs1(public_key)
    return rsa.encrypt(data, public_key)


def decrypt(data, private_key):
    private_key = rsa.PrivateKey.load_pkcs1(private_key)
    try:
        return rsa.decrypt(data, private_key)
    except rsa.DecryptionError:
        raise DecryptionError


def sign(data, private_key):
    private_key = rsa.PrivateKey.load_pkcs1(private_key)
    return rsa.sign(data, private_key, "SHA-256")


def verify(data, signature, public_key):
    public_key = rsa.PublicKey.load_pkcs1(public_key)
    try:
        rsa.verify(data, signature, public_key)
        return True
    except rsa.VerificationError:
        return False


class DecryptionError(Exception):
    pass
