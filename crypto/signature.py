import base64

from crypto import rsa


def sign(data, private_key):
    data = data.encode()
    signature = rsa.sign(data, private_key)
    
    return base64.standard_b64encode(signature + data).decode()


def decode_and_verify(data, public_key):
    data = base64.standard_b64decode(data)
    
    signature, data = data[:64], data[64:]
    
    return data.decode(), rsa.verify(data, signature, public_key)
