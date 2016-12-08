import struct

from crypto import des, rsa

KEY_LENGTH = 24


def encrypt(data, public_key):
    key = des.generate_key(KEY_LENGTH)
    encrypted_data = des.encrypt(data, key)
    
    encrypted_key = rsa.encrypt(key, public_key)
    
    key_length_bytes = struct.pack(">I", len(encrypted_key))
    
    return key_length_bytes + encrypted_key + encrypted_data


def decrypt(encrypted, private_key):
    key_length = struct.unpack(">I", encrypted[:4])[0]
    
    encrypted_key = encrypted[4:4 + key_length]
    
    key = rsa.decrypt(encrypted_key, private_key)
    
    encrypted_data = encrypted[4 + key_length:]
    
    data = des.decrypt(encrypted_data, key)
    
    return data
