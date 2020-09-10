// Server side C/C++ program to demonstrate Socket programming 
// Here's some include statements that might be helpful for you
#include <string> 
#include <cstring>
#include <iostream>
#include <stdlib.h>
#include <sys/socket.h> 
#include <netdb.h>
#include <netinet/in.h> 
#include <arpa/inet.h>
#include <stdio.h>
#include <unistd.h>

using namespace std;

int main(int argc, char const *argv[]) 
{ 
	// check to see if user input is valid
	if(argc < 3)
	{
		cerr << "Error. Usage: server ip, port, message " << endl;
	}
	char socket_read_buffer[1024];
	const char *user_message = argv[3];
	
	// TODO: Fill out the server ip and port
	std::string server_ip = argv[1];  //professor's server 34.209.114.30
	std::string server_port = argv[2]; //professor's port 5006

	int opt = 1;
	int client_fd = -1;

	// TODO: Create a TCP socket()

	client_fd = socket(AF_INET, SOCK_STREAM, 0);

	// Enable reusing address and port
	if (setsockopt(client_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) { 
		return -1;
	}

	// Check if the client socket was set up properly
	if(client_fd == -1){
		printf("Error- Socket setup failed");
		return -1;
	}
	
	// Helping you out by pepping the struct for connecting to the aws server
	struct addrinfo hints;
	struct addrinfo *server_addr;

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	int s;
	s = getaddrinfo(server_ip.c_str(), server_port.c_str(), &hints, &server_addr);
	if (s != 0) {
               printf("Address Failed \n");
           }


	
    int connect_return =  connect(client_fd, server_addr->ai_addr, server_addr->ai_addrlen);
    if (connect_return < 0) 
    { 
        printf("\nConnection Failed \n"); 
        return -1; 
    } 
	// TODO: Retreive user input

	// TODO: Send() the user input to the aws server
	send(client_fd, user_message, strlen(user_message), 0);

	// TODO: Recieve any messages from the aws server and print it here. Don't forget to make sure the string is null terminated!
	int len = recv(client_fd, socket_read_buffer, sizeof(socket_read_buffer), 0);
	socket_read_buffer[len] = '\0';
	printf("%s\n", socket_read_buffer);
	
	// TODO: Close() the socket
	close(client_fd);

	return 0; 
} 
