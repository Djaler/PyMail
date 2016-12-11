import pyDes
import rsa.randnum


def generate_key(length):
    return rsa.randnum.read_random_bits(length * 8)


def encrypt(data, key):
    des = pyDes.triple_des(key)

    return des.encrypt(data, padmode=pyDes.PAD_PKCS5)


def decrypt(data, key):
    des = pyDes.triple_des(key)

    return des.decrypt(data, padmode=pyDes.PAD_PKCS5)
