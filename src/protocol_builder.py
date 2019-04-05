import eel
from networking import send
from keys import generate_keys
from user_info import get_user_info


@eel.expose
def new_user(user_name):
    # Protocol 0
    priv, pub = generate_keys()
    header = '@' + user_name + ':0'
    priv_key = priv.decode()
    pub_key = pub.decode()
    packet = "{\"private\":\""+priv_key+"\", \"public\":\""+pub_key+"\"}"
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
    user_name, priv, pub = get_user_info()
    header = '@' + user_name + ':1'
    packet = "{\"Delete\":1, \"public\":\""+pub+"\", \"private\":\""+priv+"\"}"
    message = send([header + ' ' + packet])
    print(message)


@eel.expose
def delete_item():
    # Protocol 2
    return 'I delete items from your database'


@eel.expose
def add_item():
    # Protocol 3
    return 'I add item(s) to your database'


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
def loan_return():
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
    delete_user()

