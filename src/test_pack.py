from networking import send
from keys import generate_keys, create_item_key
import simplejson as json


# Test methods
def other_user(user_name):
    priv, pub = generate_keys()
    header = '@' + user_name + ':0'
    priv_key = priv.decode()
    pub_key = pub.decode()
    packet = json.dumps({"private": priv_key, "public": pub_key})
    send([header + ' ' + packet])
    return user_name, priv.decode(), pub.decode()


def delete_other_user(user_name, priv_key, pub_key):
    header = '@' + user_name + ':1'
    packet = json.dumps({"Delete": 1, "public": pub_key, "private": priv_key})
    send([header + ' ' + packet])


def other_add_item(item_name, category, subcategory, user_name, priv_key):
    # Protocol 3
    item = {
        "Current Owner": user_name,
        "Permanent Owner": user_name,
        "Category": category,
        "Subcategory": subcategory,
        "Name": item_name,
        "Groups": [],
        "Type Info": {},
        "Image": '',
        "User Tags": [],
    }
    item_key = create_item_key(item)
    header = '@' + user_name + ':3'
    packet = json.dumps({item_key: item, "private": priv_key})
    send([header + ' ' + packet])
    # item_key is returned for testing purposes
    return item_key
