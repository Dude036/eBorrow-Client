import socket
import time
from keys import generate_keys
import simplejson as json


# Networking Info
HOST = '127.0.0.1'  			# Localhost for testing
# HOST = '172.31.38.104'	    # AWS testing
# HOST = '192.168.1.166'	    # Accepts outside traffic !!THIS NEEDS TO STAY!!
# HOST = '24.10.208.43'			# The server's hostname or IP address

PORT = 41111	            # The port used by the server

END_BYTE = b'\x7F\xFF\x7F\xFF'
BUFF_SIZE = 8192


def recv_until(sock):
    total_data = []
    # data = b''
    start = time.time()
    timeout = 20
    while True:
        data = sock.recv(BUFF_SIZE)
        if END_BYTE in data:
            total_data.append(data[:data.find(END_BYTE)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            # check if end_of_data was split
            last_pair = total_data[-2] + total_data[-1]
            if END_BYTE in last_pair:
                total_data[-2] = last_pair[:last_pair.find(END_BYTE)]
                total_data.pop()
                break
        if time.time() - start > timeout:
            return ''
    return ''.join([thing.decode() for thing in total_data])


# expects send buffer of from [header + ' ' + packet]
def send(send_buffer):
    response = ''
    for thing in send_buffer:
        s = socket.create_connection((HOST, PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.sendall(thing.encode() + END_BYTE)
        time.sleep(1)
        response = recv_until(s)
        s.close()
    return response
