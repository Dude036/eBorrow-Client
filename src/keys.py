from OpenSSL import crypto
import hashlib


def generate_keys():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    private_key = ''.join(crypto.dump_privatekey(
        crypto.FILETYPE_PEM, k).decode().split('\n')[1:-2]).encode()
    public_key = ''.join(crypto.dump_publickey(
        crypto.FILETYPE_PEM, k).decode().split('\n')[1:-2]).encode()
    return private_key, public_key


def create_item_key(item):
    return hashlib.md5(str(item["Permanent Owner"] + item["Category"] + item["Subcategory"] + item["Name"]).encode()).hexdigest()
