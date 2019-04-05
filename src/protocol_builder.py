import eel
from networking import send
from keys import generate_keys


@eel.expose
def new_user(user_name):
    priv, pub = generate_keys()
    header = '@' + user_name + ':0'
    priv_key = priv.decode()
    pub_key = pub.decode()
    packet = "{\"private\":\"" + priv_key + "\", \"public\":\"" + pub_key + "\"}"
    message = send([header + ' ' + packet])
    print(message)
    if '16' not in message:
        # Save user name
        f = open("username.txt", "w")
        f.write(user_name)
        f.close()

        # Save private key
        f = open("private.txt", "w")
        f.write(priv_key)
        f.close()

        # Save public key
        f = open("public.txt", "w")
        f.write(pub_key)
        f.close()

        # Create file to hold future friend keys
        f = open("friends.txt", "w")
        f.close()
        return 'Congratulations on your new account'

    else:
        print('User name already in use')
        return 'User name already in use'


@eel.expose
def delete_user():
    f = open("username.txt", "r")
    user_name = f.read()
    f.close()
    f = open("private.txt", "r")
    priv = f.read()
    f.close()
    f = open("public.txt", "r")
    pub = f.read()
    f.close()
    header = '@' + user_name + ':1'
    packet = "{\"Delete\": 1, \"public\":\""+pub+"\", \"private\":\""+priv+"\"}"
    message = send([header + ' ' + packet])
    print(message)


@eel.expose
def log_in():
    name = open("username")
    user_name = name.read()
    name.close()
    key = open("keys.txt", "r")
    private_key = key.read()
    key.close()

    header = '@' + user_name + ':4'

    return


if __name__ == '__main__':
    new_user('user1')
    delete_user()

