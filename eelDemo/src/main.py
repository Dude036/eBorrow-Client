import eel
import time
import json
from networking import send
from keys import generate_keys

eel.init('web')


@eel.expose
def getTime():
    return time.strftime('%c')


@eel.expose
def getJson():
    items = ''

    with open('web/database/mystuff.json', 'r') as f:
        mystuff_dict = json.load(f)

    for mystuff in mystuff_dict:
        items += mystuff
        items += ' '

    return items


@eel.expose
def new_user(user_name):
    pri, pub = generate_keys()
    header = '@' + user_name + ':0'
    packet = "{\"private\":\"" + pri.decode() + "\", \"public\":\"" + pub.decode() + "\"}"
    message = send([header + ' ' + packet])
    print(message)
    if '16' not in message:
        # Save user name
        f = open("username.txt", "a")
        f.write(user_name)
        f.write('\n')
        f.close()

        # Save private key
        f = open("private.txt", "a")
        f.write(pri.decode())
        f.write('\n')
        f.close()

        # Save public key
        f = open("public.txt", "a")
        f.write(pub.decode())
        f.write('\n')
        f.close()

        # Create file to hold future friend keys
        f = open("friends.txt", "a")
        f.close()
        return

    else:
        print('not adding this one')
        return 'User name is already taken'


@eel.expose
def delete_user():
    f = open("username.txt", "r")
    user_name = f.read()
    f.close()
    f = open("private.txt", "r")
    pri = f.read()
    f.close()
    f = open("public.txt", "r")
    pub = f.read()
    f.close()
    header = '@' + user_name + ':1'
    packet = '{\"Delete\": a, \"public\":'+pub+', \"private\":'+pri+'}'
    send([header + ' ' + packet])


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


eel.start('html/hello.html', block=False)

while True:
    eel.sleep(10)

