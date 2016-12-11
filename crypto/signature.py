import base64

from crypto import rsa


def sign(data, private_key):
    signature = rsa.sign(data, private_key)

    return base64.standard_b64encode(signature + data)


def decode_and_verify(data, public_key):
    data = base64.standard_b64decode(data)
    
    signature, data = data[:64], data[64:]

    return data, rsa.verify(data, signature, public_key)
