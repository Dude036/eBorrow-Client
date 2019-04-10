import eel
import os
from networking import send
from keys import generate_keys, create_item_key
from user_info import get_username, get_priv_key, get_pub_key
import simplejson as json
from test_pack import other_user, other_add_item, delete_other_user


@eel.expose
def new_user(user_name):
    # TODO don't let this run if there is already a user on the machine
    # TODO May need to add a nuke user if we run a second new_user
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
        f = open("friends.json", "w")
        f.write('{}')
        f.close()

        # Create user item database
        f = open("./web/db/mine.json", "w")
        f.write('{}')
        f.close()

        # Create friends item database
        f = open("./web/db/theirs.json", "w")
        f.write('{}')
        f.close()
        return True

    else:
        print('User name already in use')
        return False


@eel.expose
def delete_user():
    # Protocol 1
    user_name = get_username()
    priv_key = get_priv_key()
    pub_key = get_pub_key()
    header = '@' + user_name + ':1'
    packet = json.dumps({"Delete": 1, "public": pub_key, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)


@eel.expose
def delete_item(item_key):
    # Protocol 2
    user_name = get_username()
    priv_key = get_priv_key()
    header = '@' + user_name + ':2'
    packet = json.dumps({"Key": [item_key], "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    return 'I delete items from your database'


@eel.expose
def add_item(item_name, category, subcategory, other_info):
    # Protocol 3
    # TODO may want to add a send all or send some function for own stuff after this call
    user_name = get_username()
    priv_key = get_priv_key()
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
    # item_key is returned for testing purposes
    return item_key


@eel.expose
def send_all():
    # Protocol 4
    # TODO detect when the received packet is not an id 200
    my_dir = './web/db/'
    user_name = get_username()
    pub_key = get_pub_key()
    header = '@' + user_name + ':4'
    packet = json.dumps({"public": pub_key, "Library": 1})
    message = send([header + ' ' + packet])
    message = message.split(' ', 1)[1]
    f = open(os.path.join(my_dir, "mine.json"), "w")
    f.write(message)
    f.close()

    f = open(os.path.join(my_dir, "theirs.json"), "r")
    friend_library = f.read()
    f.close()
    friend_library = json.loads(friend_library)

    friends = open("friends.json", "r")
    for friend in friends:
        friend_key = friend
        json.dumps({"public": friend_key, "Library": 1})
        a_friend = send([header + ' ' + packet])
        a_friend = a_friend.split(' ', 1)[1]
        a_friend = json.loads(a_friend)
        for item in a_friend:
            friend_library[item] = a_friend[item]
    friends.close()

    f = open(os.path.join(my_dir, "theirs.json"), "w")
    friend_library = json.dumps(friend_library)
    f.write(friend_library)
    f.close()

    return 'I get you all of your stuff and your friends'


@eel.expose
def send_some():
    # Protocol 5
    # Most likely to be used just after you add an item to have just it added to your local db
    return 'I get you specific information'


@eel.expose
def change_owner():
    # Protocol 6
    return 'I change current owner'


@eel.expose
def send_message():
    # Protocol 7.
    print('in send message')
    user_name = get_username()
    priv_key = get_priv_key()
    header = '@' + user_name + ':7'
    packet = json.dumps({"Messages": 1, "private": priv_key})
    print('sending request')
    message = send([header + ' ' + packet])
    print('received request')
    print(message)
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
    # Make some friends to practice with
    use1, priv1, pub1 = other_user('friend1')
    use2, priv2, pub2 = other_user('friend2')

    # Give friends some stuff
    other_1 = other_add_item('a sweet show', 'Entertainment', 'Movie', use1, priv1)
    other_2 = other_add_item('a sweet show', 'Entertainment', 'Movie', use1, priv1)
    other_3 = other_add_item('a sweet show', 'Entertainment', 'Movie', use2, priv2)
    other_4 = other_add_item('a sweet show', 'Entertainment', 'Movie', use2, priv2)

    # Code to put friends pub keys where we can read over them
    f = open("friends.json", "r")
    friends = f.read()
    f.close()
    friends = json.loads(friends)
    friends[use1] = pub1
    friends[use2] = pub2
    friends = json.dumps(friends)
    f = open("friends.json", "w")
    f.write(friends)
    f.close()

    # Test each protocol
    key1 = add_item('a good movie title', 'Entertainment', 'Movie', 'some other cool stuff')
    key2 = add_item('another great flick', 'Entertainment', 'Movie', 'some other cool stuff')
    send_all()
    delete_item(key1)
    delete_item(key2)
    send_message()

    delete_user()
    delete_other_user(use1, priv1, pub1)
    delete_other_user(use2, priv2, pub2)
