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


eel.start('html/hello.html', block=False)

while True:
    eel.sleep(10)

