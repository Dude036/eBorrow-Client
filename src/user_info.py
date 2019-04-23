import eel

@eel.expose
def get_username():
    f = open("username.txt", "r")
    user_name = f.read()
    f.close()
    return user_name


def get_priv_key():
    f = open("private.txt", "r")
    priv_key = f.read()
    f.close()
    return priv_key


def get_pub_key():
    f = open("public.txt", "r")
    pub_key = f.read()
    f.close()
    return pub_key
