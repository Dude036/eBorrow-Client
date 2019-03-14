import eel
import time
import json

eel.init('web')


@eel.expose
def getTime():
    return time.strftime('%c')


@eel.expose
def getJson():
    items = ''

    with open('mystuff.json', 'r') as f:
        mystuff_dict = json.load(f)

    for mystuff in mystuff_dict:
        items += mystuff
        items += ' '


    return items


eel.start('hello.html', block=False)

while True:
    eel.sleep(10)
