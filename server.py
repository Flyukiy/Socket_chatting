# Import socket module
from socket import *
import threading
import sys  # In order to terminate the program

FLAG = False  # this is a flag variable for checking quit

# function for receiving message from client


def recv_from_client(conn):
    global FLAG
    try:
        # Receives the request message from the client
        while True:
            if FLAG == True:
                break
            message = conn.recv(1024).decode()
            # if 'q' is received from the client the server quits
            if message == 'q':
                conn.send('q'.encode())
                print('Closing connection')
                conn.close()
                FLAG = True
                break
            print('Client: ' + message)
    except:
        conn.close()


# function for receiving message from client
def send_to_client(conn):
    global FLAG
    try:
        while True:
            if FLAG == True:
                break
            send_msg = input('')
            # the server can provide 'q' as an input if it wish to quit
            if send_msg == 'q':
                conn.send('q'.encode())
                print('Closing connection')
                conn.close()
                FLAG = True
                break
            conn.send(send_msg.encode())
    except:
        conn.close()


# this is main function
def main():
    threads = []
    global FLAG

    # TODO (1) - define HOST name, this would be an IP address or 'localhost' (1 line)
    HOST = 'localhost'
    # TODO (2) - define PORT number (1 line) (Google, what should be a valid port number)
    # make sure the ports are not used for any other application
    serverPort = 6789

    # Create a TCP server socket
    #(AF_INET is used for IPv4 protocols)
    #(SOCK_STREAM is used for TCP)
    # TODO (3) - CREATE a socket for IPv4 TCP connection (1 line)
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Bind the socket to server address and server port
    # TODO (4) - bind the socket for HOSR and serverPort (1 line)
    serverSocket.bind((HOST, serverPort))

    # Listen to at most 1 connection at a time
    # TODO (5) - listen and wait for request from client (1 line)
    serverSocket.listen(1)

    # Server should be up and running and listening to the incoming connections
    print('The chat server is ready to connect to a chat client')
    # TODO (6) - accept any connection request from a client (1 line)
    connectionSocket, addr = serverSocket.accept()
    print('Sever is connected with a chat client\n')

    t_rcv = threading.Thread(target=recv_from_client, args=(connectionSocket,))
    t_send = threading.Thread(target=send_to_client, args=(connectionSocket,))
    # call the function to receive message server
    # recv_from_server(clientSocket)
    threads.append(t_rcv)
    threads.append(t_send)
    t_rcv.start()
    t_send.start()

    t_rcv.join()
    t_send.join()

    # closing serverScoket before exiting
    print('EXITING')
    serverSocket.close()
    # Terminate the program after sending the corresponding data
    sys.exit()


# This is where the program starts
if __name__ == '__main__':
    main()
