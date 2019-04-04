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
    error = send([header + ' ' + packet])

    # Check to make sure name is not already taken first.
    f = open("username.txt", "a")
    f.write(user_name)
    f.write('\n')
    f.close()

    # Make sure to create the file that will contain friends keys.
    f = open("friends.txt", "a")
    f.close()
    return


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

