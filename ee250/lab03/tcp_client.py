"""
Server IP is 52.88.20.156, ports are 5000-5008, socket is UNIX TCP 
Server receiver buffer is char[256]
If correct, the server will send a message back to you saying "I got your message"
Write your socket client code here in python
Establish a socket connection -> send a short message -> get a message back -> ternimate
"""
import socket

HOST = '3.129.247.87'  # The server's hostname or IP address
PORT = 5000       # The port used by the server

def main():

	user_input = input("Enter a message ")
	user_input = user_input.encode('UTF-8')

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	    s.connect((HOST, PORT))
	    s.sendall(user_input)
	    data = s.recv(1024)
	    data = data.decode('UTF-8')
	print('Received', data)

if __name__ == '__main__':
    main()

import socket



