import eel
import os
from networking import send
from keys import generate_keys, create_item_key
from user_info import get_username, get_priv_key, get_pub_key
import simplejson as json
from test_pack import other_user, other_add_item, delete_other_user


@eel.expose
def new_user(username):
    # TODO don't let this run if there is already a user on the machine
    # TODO May need to add a nuke user if we run a second new_user
    # Protocol 0
    priv, pub = generate_keys()
    header = '@' + username + ':0'
    priv_key = priv.decode()
    pub_key = pub.decode()
    packet = json.dumps({"private": priv_key, "public": pub_key})
    message = send([header + ' ' + packet])
    print(message)
    if '16' not in message:
        # Save user name
        f = open("username.txt", "w")
        f.write(username)
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

        if not os.path.exists('./web/db'):
            os.mkdir('./web/db')

        # Create user item database
        f = open("./web/db/mine.json", "w")
        f.write('{}')
        f.close()

        # Create message database
        f = open("./web/db/messages.json", "w")
        f.write('{"messages":[] ,"exchanges":[], "pending exchanges":[], "pending friends":[]}')
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
    username = get_username()
    priv_key = get_priv_key()
    pub_key = get_pub_key()
    header = '@' + username + ':1'
    packet = json.dumps({"Delete": 1, "public": pub_key, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)


@eel.expose
def delete_item(item_key):
    # Protocol 2
    username = get_username()
    priv_key = get_priv_key()
    header = '@' + username + ':2'
    packet = json.dumps({"Key": [item_key], "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    return 'I delete items from your database'


@eel.expose
def add_item(item_name, category, subcategory, groups, type, user_tag):
    # Protocol 3
    # TODO may want to add a send all or send some function for own stuff after this call
    username = get_username()
    priv_key = get_priv_key()
    item = {
        "Current Owner": username,
        "Permanent Owner": username,
        "Category": category,
        "Subcategory": subcategory,
        "Name": item_name,
        "Groups": [],
        "Type Info": {},
        "Image": '',
        "User Tags": [],
    }
    groups = groups.split(" ")
    for i in groups:
        item["Groups"].append(i)
    item["Type Info"] = type
    user_tag = user_tag.split(" ")
    for j in user_tag:
        item["User Tags"].append(j)
    item_key = create_item_key(item)

    header = '@' + username + ':3'
    packet = json.dumps({item_key: item, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    print(header)
    # item_key is returned for testing purposes
    return item_key


@eel.expose
def send_all():
    # Protocol 4
    # TODO detect when the received packet is not an id 200
    my_dir = './web/db/'
    username = get_username()
    pub_key = get_pub_key()
    header = '@' + username + ':4'
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

    f = open("friends.json", "r")
    my_friends = f.read()
    f.close()
    my_friends = json.loads(my_friends)

    for friend in my_friends:
        header = '@' + friend + ':4'
        packet = json.dumps({"public": my_friends[friend], "Library": 1})
        a_friend = send([header + ' ' + packet])
        a_friend = a_friend.split(' ', 1)[1]
        a_friend = json.loads(a_friend)
        for item in a_friend:
            friend_library[item] = a_friend[item]

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
def change_owner(item_key, friend_name, in_date, out_date):
    # Protocol 6
    # permanent owner agrees to loan item, this protocol is sent
    username = get_username()
    priv_key = get_priv_key()
    f = open("friends.json", "r")
    friend_list = f.read()
    f.close()
    friend_list = json.loads(friend_list)

    header = '@' + username + ':6'
    packet = {}
    packet['key'] = item_key
    packet['New Owner'] = friend_name
    packet['public'] = friend_list[friend_name]
    packet['private'] = priv_key
    packet['Schedule']['In'] = in_date
    packet['Schedule']['Out'] = out_date
    packet = json.dumps(packet)

    message = send([header + ' ' + packet])
    print(message)

    return 'I change current owner'


@eel.expose
def send_message():
    # Protocol 7
    username = get_username()
    priv_key = get_priv_key()
    header = '@' + username + ':7'
    packet = json.dumps({"Messages": 1, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    message = message.split("[")
    message = message[1]
    message = message.replace("]", "")
    message = message.split(", ")
    f = open("./web/db/messages.json", "r")
    message_db = f.read()
    f.close()
    message_db = json.loads(message_db)
    for i in message:
        message_db["messages"].append(i)
    message_db = json.dumps(message_db)
    f = open("./web/db/messages.json", "w")
    f.write(message_db)
    f.close()
    return 'I get you all of the messages from your "inbox"'


@eel.expose
def send_exchange():
    # Protocol 8
    username = get_username()
    priv_key = get_priv_key()
    header = '@' + username + ':8'
    packet = json.dumps({"Exchanges": 1, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    message = message.split("[")
    message = message[1]
    message = message.replace("]", "")
    message = message.split(", ")
    f = open("./web/db/messages.json", "r")
    message_db = f.read()
    f.close()
    message_db = json.loads(message_db)
    for i in message:
        message_db["exchanges"].append(i)
    message_db = json.dumps(message_db)
    f = open("./web/db/messages.json", "w")
    f.write(message_db)
    f.close()
    return 'I get you all of your exchanges'


@eel.expose
def clear_messagese():
    username = get_username()
    priv_key = get_priv_key()
    header = '@' + username + ':9'
    packet = json.dumps({"Messages": -1, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)


@eel.expose
def send_pending_friends():
    # TODO need to implement remove friend.
    username = get_username()
    priv_key = get_priv_key()
    header = '@' + username + ':10'
    packet = json.dumps({"Friends": 1, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    message = message.split("[")
    message = message[1]
    message = message.replace("]", "")
    message = message.split(", ")
    f = open("./web/db/messages.json", "r")
    message_db = f.read()
    f.close()
    message_db = json.loads(message_db)
    for i in message:
        # read over each item and either add it or remove a friend
        # if i
        message_db["pending friends"].append(i)
    message_db = json.dumps(message_db)
    f = open("./web/db/messages.json", "w")
    f.write(message_db)
    f.close()


@eel.expose
def send_pending_exchanges():
    username = get_username()
    priv_key = get_priv_key()
    header = '@' + username + ':11'
    packet = json.dumps({"Exchanges": 1, "private": priv_key})
    message = send([header + ' ' + packet])
    print(message)
    message = message.split("{")
    message = message[1]
    message = message.replace("}", "")
    message = message.split(", ")
    f = open("./web/db/messages.json", "r")
    message_db = f.read()
    f.close()
    message_db = json.loads(message_db)
    for i in message:
        message_db["pending exchanges"].append(i)
    message_db = json.dumps(message_db)
    f = open("./web/db/messages.json", "w")
    f.write(message_db)
    f.close()


@eel.expose
def item_request(item_hash, friend_name):
    # Protocol 100
    username = get_username()
    pub_key = get_pub_key()
    # print(pub_key)
    # pub_key = "pub_key"
    header = '@' + username + ':100'

    borrower_info = {"Public": pub_key, "Username": username}
    f = open("friends.json", "r")
    my_friends = f.read()
    f.close()
    my_friends = json.loads(my_friends)
    friend_key = my_friends[friend_name]
    # print(friend_key)
    # friend_key = "friend_key"
    lender_info = {"Public": friend_key, "Username": friend_name}

    packet = {}
    packet["Key"] = item_hash
    packet["Borrower"] = borrower_info
    packet["Lender"] = lender_info
    # print(packet)
    packet = json.dumps(packet)
    message = send([header + ' ' + packet])
    print(message)

    return 'I request items'


@eel.expose
def friend_request(friend_name):
    # Protocol 101
    username = get_username()
    header = '@' + username + ':101'
    packet = json.dumps({"Target": friend_name})
    message = send([header + ' ' + packet])
    print(message)
    return 'I request friends'


@eel.expose
def add_friend(friend_name):
    # Protocol 102
    username = get_username()
    pub_key = get_pub_key()
    header = '@' + username + ':102'
    packet = {}
    packet["Target"] = friend_name
    packet["Key"] = pub_key
    packet = json.dumps(packet)
    message = send([header + ' ' + packet])
    print(message)
    return 'I accept friend requests'


@eel.expose
def delete_friend(friend_name):
    # Protocol 103
    username = get_username()
    header = '@' + username + ':103'
    packet = json.dumps({"Target": friend_name})
    message = send([header + ' ' + packet])
    print(message)
    return 'I delete friends'


if __name__ == '__main__':
    print('new user')
    new_user('user1')
    # Make some friends to practice with
    use1, priv1, pub1 = other_user('friend1')
    use2, priv2, pub2 = other_user('friend2')

    # Give friends some stuff
    other_1 = other_add_item('a sweet show', 'Entertainment', 'Movie', use1, priv1)
    other_2 = other_add_item('a super great show', 'Entertainment', 'Movie', use1, priv1)
    other_3 = other_add_item('a sweet show', 'Entertainment', 'Movie', use2, priv2)
    other_4 = other_add_item('a totally different show show', 'Entertainment', 'Movie', use2, priv2)

    # Code to put friends pub keys where we can read over them
    file = open("friends.json", "r")
    friends = file.read()
    file.close()
    friends = json.loads(friends)
    friends[use1] = pub1
    friends[use2] = pub2
    friends = json.dumps(friends)
    file = open("friends.json", "w")
    file.write(friends)
    file.close()

    # Test each protocol
    print('add item')
    key1 = add_item('a good movie title', 'Entertainment', 'Movie', 'men women people', 'it is in good condition', 'action romance cartoon')
    key2 = add_item('another great flick', 'Entertainment', 'Movie', 'men', 'it is in good condition', 'action')
    print('send all')
    send_all()
    print('delete item')
    delete_item(key1)
    delete_item(key2)
    print('send messages')
    send_message()
    send_exchange()
    send_pending_exchanges()
    send_pending_friends()
    print('item request')
    item_request(other_1, use1)
    # print('friend request')
    # friend_request(use2)
    # print('add friend')
    # add_friend(use2)
    # print('delete friend')
    # delete_friend(use2)

    print('delete user')
    delete_user()
    delete_other_user(use1, priv1, pub1)
    delete_other_user(use2, priv2, pub2)
