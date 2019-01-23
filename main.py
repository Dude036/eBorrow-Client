#!/usr/bin/python3

import socket
import simplejson as json
from pprint import pprint
import time


HOST = '24.10.208.43'	# The server's hostname or IP address
PORT = 41111		# The port used by the server

Items = json.load(open("db.json", 'r'))

def dictionary_to_byte_string(dictionary):
	return json.dumps(dictionary)

if __name__ == '__main__':
	send_buffer = []

	for key, value in Items.items():
		send_buffer.append('<' + key + '> ' + dictionary_to_byte_string(value))


	for thing in send_buffer:
		# Send Buffer
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.connect((HOST, PORT))
			s.sendall(thing.encode())
		print("Sent:", thing[:34])
		time.sleep(.2)
