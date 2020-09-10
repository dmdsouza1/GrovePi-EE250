"""
Server IP is 52.88.20.156, ports are 5000-5008, socket is UNIX TCP 
Server receiver buffer is char[256]
If correct, the server will send a message back to you saying "I got your message"
Write your socket client code here in python
Establish a socket connection -> send a short message -> get a message back -> ternimate
"""
import socket

#HOST = '3.129.247.87'  # Custom EC2 server IP address
HOST = '34.209.114.30'   #professor's server IP address
PORT = 5006       # The port used by the server

def main():

	user_input = input("Enter a message ")
	user_input = user_input.encode('UTF-8')

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	    s.connect((HOST, PORT))
	    print("Connection succesful")
	    s.sendall(user_input)
	    data = s.recv(1024)
	    data = data.decode('UTF-8')
	print(data)

if __name__ == '__main__':
    main()

import socket



