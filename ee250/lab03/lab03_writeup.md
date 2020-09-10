A
Question 1

The reliabilty of UDP dropped when I added 50% loss. This occured because UDP is a best effort protocol that does not deliver the message reliably 

Question 2

TCP protocol still reliably sent the data. This is because the is more error checking and dropped packet detection on TCP protocol.

Question 3
The speed dropped drastically. This happened because it tried to send the packet that had dropped and held up the other packets in the buffer.

C

Question 1

argc and *argv[] are commandline arguments that are passed to main()
argc is the number of arguments passed in the command line
argv[] is a char pointer array to the list of the arguments passed in the command line.

Question 2

A file descriptor is a number that uniquely identifies an open file/socket resources in a computer's operating system
A file descriptor table is a table of the file/souket resource to an integer number that uniquely identifies it.

Question 3

A struct is a user-defined data type that is compromised of other data types. 

struct sockaddr_in {
               sa_family_t    sin_family; /* address family: AF_INET */
               in_port_t      sin_port;   /* port in network byte order */
               struct in_addr sin_addr;   /* internet address */
           };

Question 4

int socket(int domain, int type, int protocol)
The input parameters are the following:
Domain argument specifies a communication domain
Socket has the indicated type, which specifies the communication semantics
The protocol specifies a particular protocol to be used with the socket

Question 5
bind()

int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen)

The input parameters are the following:
the file descriptor sockfd
the address specified by addr to the socket referred to by the file descriptor sockfd
addrlen specifies the size, in bytes, of the address structure pointed to by addr



listen()
int listen(int sockfd, int backlog)

The input parameters are the following:

The sockfd argument is a file descriptor that refers to a socket of type SOCK_STREAM or SOCK_SEQPACKET

The backlog argument defines the maximum length to which the queue of pending connections for sockfd may grow

Question 6

while(1) creates an infinite loop that helps listen constantly for a message and read it into the buffer[256]
If there are multiple simultaneous connections the code will read in one at a time and not be able to process simultaneous messages

Questions 7

fork() can be used to fork off a new process to handle each new connection
