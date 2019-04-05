def get_user_info():
    f = open("username.txt", "r")
    user_name = f.read()
    f.close()
    f = open("private.txt", "r")
    priv = f.read()
    f.close()
    f = open("public.txt", "r")
    pub = f.read()
    f.close()
    return user_name, priv, pub
