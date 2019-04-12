import eel
<<<<<<< HEAD
import time
import json
from protocol_builder import new_user
=======
>>>>>>> 08573c0f05a39ebbec20b136336a2ff1666893a7

eel.init('web')


<<<<<<< HEAD
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


=======
>>>>>>> 08573c0f05a39ebbec20b136336a2ff1666893a7
eel.start('html/login.html', block=False)

while True:
    eel.sleep(10)

