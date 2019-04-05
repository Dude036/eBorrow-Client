from networking import send
from keys import generate_keys


def new_user(user_name):
    pri, pub = generate_keys()

    # Save user name
    f = open("username.txt", "w")
    f.write(user_name)
    f.close()

    # Save private key
    f = open("private.txt", "w")
    pri_key = pri.decode()
    f.write(pri_key)
    f.close()

    # Save public key
    f = open("public.txt", "w")
    pub_key = pub.decode()
    f.write(pub_key)
    f.close()

    # Create file to hold future friend keys
    f = open("friends.txt", "w")
    f.close()

    header = '@' + user_name + ':0'
    packet = "{\"private\":\"" + pri_key + "\", \"public\":\"" + pub_key + "\"}"
    message = send([header + ' ' + packet])
    print(message)
    if '16' in message:
        # Save user name
        f = open("username.txt", "w")
        f.write('')
        f.close()

        # Save private key
        f = open("private.txt", "w")
        f.write('')
        f.close()

        # Save public key
        f = open("public.txt", "w")
        f.write('')
        f.close()
        return 'User name is already in use'

    else:
        print('congrats on new account')
        return 'Congrats on new account'

# Is read out of file adding something to make it wrong? Like whitespace on the end?
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
    packet = "{\"Delete\": 1, \"public\":\""+pub+"\", \"private\":\""+pri+"\"}"
    message = send([header + ' ' + packet])
    print(message)

    if 'MIIJQgIBADANBgkqhkiG9w0BAQEFAASCCSwwggkoAgEAAoICAQDLVw3J5PBiWCLBU+eYNpDkn37vItCB/RgIHBQJeQQfwsSruYArqEsQY4fsip3iCF0i0tOt' == 'MIIJQgIBADANBgkqhkiG9w0BAQEFAASCCSwwggkoAgEAAoICAQDLVw3J5PBiWCLBU+eYNpDkn37vItCB/RgIHBQJeQQfwsSruYArqEsQY4fsip3iCF0i0tOt':
        print('they are same')


if __name__ == '__main__':
    new_user('user1')
    delete_user()

