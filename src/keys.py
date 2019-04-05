from OpenSSL import crypto


def generate_keys():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)
    private_key = ''.join(crypto.dump_privatekey(
        crypto.FILETYPE_PEM, k).decode().split('\n')[1:-2]).encode()
    public_key = ''.join(crypto.dump_publickey(
        crypto.FILETYPE_PEM, k).decode().split('\n')[1:-2]).encode()

    # Need to decide how to save keys
    # pri = open("my private.txt", "a")
    # pri.write(private_key.decode())
    # pri.close()
    # pub = open("my public.txt", "a")
    # pub.write(public_key.decode())
    # pub.close()

    return private_key, public_key
