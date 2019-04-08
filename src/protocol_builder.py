import eel
from networking import send
from keys import generate_keys, create_item_key
from user_info import get_user_info
import simplejson as json


@eel.expose
def new_user(user_name):
    # TODO don't let this run if there is already a user on the machine
    # Protocol 0
    priv, pub = generate_keys()
    header = '@' + user_name + ':0'
    priv_key = priv.decode()
    pub_key = pub.decode()
    packet = json.dumps({"private": priv_key, "public": pub_key})
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
    # Protocol 1
    user_name, priv_key, pub_key = get_user_info()
    header = '@' + user_name + ':1'
    packet = json.dumps({"Delete": 1, "public": pub_key, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)


@eel.expose
def delete_item(item_key):
    # Protocol 2
    user_name, priv_key, pub_key = get_user_info()
    header = '@' + user_name + ':2'
    packet = json.dumps({"Key": [item_key], "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    return 'I delete items from your database'


@eel.expose
def add_item(item_name, category, subcategory, other_info):
    # Protocol 3
    user_name, priv_key, pub_key = get_user_info()
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
    message = send([header + ' ' + packet])
    print(message)
    return item_key


# Primarily called to initialize local database
@eel.expose
def send_all():
    # Protocol 4
    return 'I get you all of your stuff and your friends'


@eel.expose
def send_some():
    # Protocol 5
    return 'I get you specific information'


@eel.expose
def change_owner():
    # Protocol 6
    return 'I change current owner'


@eel.expose
def send_message():
    # Protocol 7
    return 'I send a message'


@eel.expose
def send_exchange():
    # Protocol 8
    return 'I send exchanges'


@eel.expose
def item_request():
    # Protocol 100
    return 'I request items'


@eel.expose
def friend_request():
    # Protocol 101
    return 'I request friends'


@eel.expose
def add_friend():
    # Protocol 102
    return 'I accept friend requests'


@eel.expose
def delete_friend():
    # Protocol 103
    return 'I delete friends'


@eel.expose
def return_items():
    # Protocol 200
    return 'I return items to their owners'


@eel.expose
def return_messages():
    # Protocol 201
    return 'I reply to messages'


@eel.expose
def return_exchanges():
    # Protocol 202
    return 'I do something'


if __name__ == '__main__':
    new_user('user1')
    key = add_item('a good movie title', 'Entertainment', 'Movie', 'some other cool stuff')
    delete_item(key)
    delete_user()
